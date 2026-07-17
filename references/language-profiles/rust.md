# Rust 语言剖面

> 供 `ddd-port-scaffold` 与各分层实现能力（`ddd-domain-impl` / `ddd-application-impl` / `ddd-inbound-adapter-impl` / `ddd-outbound-adapter-impl` / `cqrs-read-model-impl`）使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | Rust 惯用法 |
| :--- | :--- |
| 端口/接口 | `trait` |
| 聚合根/实体 | `struct` + `impl`，方法内部强制不变量 |
| 值对象 | `struct` + `#[derive(Clone, PartialEq, Eq)]` |
| 不可变性 | 默认不可变；字段非 pub，强制走受控构造 |
| 按值相等 | `#[derive(PartialEq, Eq)]` |
| 标识（ID）类型 | newtype `struct OrderId(Uuid)` |
| 领域事件 | `struct`（或 `enum` 事件集） |
| 拒绝非法操作 | 构造期校验返回 `Result<Self, DomainError>`；方法以 `Result<_, DomainError>` 拒绝；`panic!` 仅留给"不可能违反"的内部断言 |
| 空值/缺失 | `Option<T>` |
| 仓储接口位置 | 领域 crate |

- 非法状态不可构造：用 `enum` 把状态机建成类型（不同状态不同类型/变体），非法转移编译期即不存在。
- 领域错误用 thiserror 定义 `enum DomainError`（`OrderAlreadyConfirmed` 为变体），不外泄 `sqlx::Error`。

端口骨架（中立契约 `OrderRepository`）：

```rust
trait OrderRepository {
    fn find_by_id(&self, id: OrderId) -> Option<Order>;       // 单聚合查询
    fn save(&self, order: &Order) -> Result<(), DomainError>; // 1 聚合/1 事务
}
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释随骨架保留。异步 trait 二选一：**泛型静态分发**（`struct Handler<R: OrderRepository>`）可用 Rust 1.75+ 原生 `async fn` in trait；**需要 `dyn` 动态分发**（如 `Arc<dyn OrderRepository>`）时原生 async fn 不满足对象安全，须用 `#[async_trait]`（boxed future）或让 trait 方法显式返回 `Pin<Box<dyn Future<…>>>`。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | 每用例一个 struct，单方法 `async fn handle(&self, cmd) -> Result<_, AppError>`；端口依赖首选泛型静态分发（原生 async fn trait），要 `Arc<dyn Trait>` 则配 `#[async_trait]` |
| Unit of Work / 事务边界 | 应用层只依赖自定义 `UnitOfWork` 端口 trait（如 `async fn execute(&self, work) -> Result<_>`）；sqlx `Transaction<'_>` 属出站适配器内部实现细节，不出现在应用层签名；1 用例 = 1 事务 |
| Result/错误映射 | thiserror 定义分层 `AppError`，`#[from] DomainError` + `?` 传播；边缘统一映射 HTTP |
| 异步语义 | tokio + `async/await`；泛型端口用原生 async fn in trait，`dyn` 端口用 `#[async_trait]`；跨任务传递注意 `Send + Sync` 约束 |
| 幂等执行器 | 幂等键表 + 唯一约束，与业务写同一事务；定义为应用层 trait，实现放基础设施 crate |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | 普通 struct + `#[derive(sqlx::FromRow, serde::Serialize)]` |
| 查询侧映射 | 查询函数直接 SQL → DTO（sqlx `query_as!`）；绕过聚合与领域 trait |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | axum / actix-web handler：提取器解析请求 → Command → 调 Input Port |
| 消息 | rdkafka StreamConsumer 循环：反序列化 → 调 Input Port |
| Job | tokio-cron-scheduler：组 Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | 基础设施 crate 内 struct `impl OrderRepository`（sqlx / diesel / SeaORM）；领域模型↔行结构显式映射 |
| Outbox | 与聚合写同事务插 outbox 表 + tokio 后台任务投递 |
| 外部网关 ACL | Gateway struct + reqwest；外部响应经 serde 类型解析后翻译成领域类型 |

## Composition Root（组合根）

- `main()` 手工装配是惯用做法：自底向上构造适配器，注入 handler；无主流 DI 容器。
- 注入方式二选一：泛型（编译期单态化，性能好）或 `Arc<dyn Trait>`（运行时分发，签名简洁）。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| cargo workspace 多 crate | 依赖方向编译期强制：Cargo.toml 未声明的 crate 根本 import 不了 |
| cargo-deny | 依赖策略审计（许可证、来源、重复依赖） |

## 测试框架与包可见性

- 测试：内建 `#[test]` + `cargo test`；trait mock 用 mockall；属性测试用 proptest。
- 保护领域内核：`pub(crate)` / 非 pub 字段强制走受控构造；领域 crate 的 Cargo.toml 不声明任何基础设施依赖（编译期零依赖保证）。
