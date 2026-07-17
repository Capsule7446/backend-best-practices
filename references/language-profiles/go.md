# Go 语言剖面

> 供 `backend-best-practices:ddd-port-scaffold` / `backend-best-practices:ddd-adapter-impl` 及 Application/读侧相关 skill 使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | Go 惯用法 |
| :--- | :--- |
| 端口/接口 | `interface`（小接口，消费方定义或领域包定义） |
| 聚合根/实体 | `struct` + 方法（指针接收器承载行为，方法内部强制不变量） |
| 值对象 | `struct`（值语义） |
| 不可变性 | 无 setter + 值传递；字段小写不导出，构造函数校验 |
| 按值相等 | 手写 `Equal()` |
| 标识（ID）类型 | 命名 `type`（`type OrderID string`） |
| 领域事件 | `struct` |
| 拒绝非法操作 | 返回 `(T, error)`，error 为领域错误值（哨兵 `var ErrOrderAlreadyConfirmed = errors.New(...)`） |
| 空值/缺失 | 返回 `nil` + 哨兵 error |
| 仓储接口位置 | 领域包 |

- 非法状态不可构造：构造函数 `NewOrder(...) (*Order, error)` 校验后才返回实例。
- 错误用 `errors.Is/As` 判别领域错误值，不外泄 `sql.ErrNoRows` 等底层错误。

端口骨架（中立契约 `OrderRepository`）：

```go
type OrderRepository interface {
    FindById(ctx context.Context, id OrderID) (*Order, error) // 单聚合查询
    Save(ctx context.Context, o *Order) error                 // 1 聚合/1 事务
}
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释随骨架保留，不随语言丢失。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | 每用例一个 struct 持端口依赖，单方法 `Handle(ctx context.Context, cmd ConfirmOrder) error` |
| Unit of Work / 事务边界 | 事务管理器 `WithinTx(ctx, func(ctx) error)`：把 `*sql.Tx` 藏进 ctx 或显式传给仓储；1 用例 = 1 事务 |
| Result/错误映射 | `(T, error)` 返回；应用层用 `fmt.Errorf("...: %w", err)` 包装补充上下文，边缘 `errors.Is/As` 判别 |
| 异步语义 | 无 async 关键字：`context.Context` 第一参数贯穿（取消/超时）；handler 内保持同步直线代码 |
| 幂等执行器 | 幂等键表 + 唯一索引，与业务写同一事务；定义为应用层接口，实现放基础设施 |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | 普通 `struct` DTO |
| 查询侧映射 | sqlc 生成查询直接扫描进 DTO / sqlx `Get`/`Select`；查询函数不经过聚合 |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | `net/http` / chi / gin handler：解析请求 → Command → 调 Input Port |
| 消息 | Kafka consumer 循环（segmentio/kafka-go）：反序列化 → 调 Input Port |
| Job | robfig/cron：组 Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | 基础设施包 struct 实现领域接口（database/sql / sqlc）；领域模型↔行结构显式映射 |
| Outbox | 与聚合写同事务插 outbox 表 + poller goroutine 投递；Watermill Forwarder 有现成实现 |
| 外部网关 ACL | Gateway struct + `net/http` client；外部响应结构翻译成领域类型后才返回 |

## Composition Root（组合根）

- `main()` 手工装配是惯用做法：自底向上 new 适配器 → 注入 handler → 注入入站适配器。
- 装配代码规模大时用 google/wire 编译期生成；避免运行时反射容器。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| `internal/` 目录 | 编译期防止外部模块 import，天然守护边界 |
| depguard（golangci-lint） | 禁止 domain 包 import infrastructure/框架包 |
| go-arch-lint | 声明式分层依赖规则检查 |

## 测试框架与包可见性

- 测试：标准 `testing` + testify，表驱动测试；集成测试用 Testcontainers for Go。
- 保护领域内核：小写标识符不导出 + `internal/` 目录；领域包只依赖标准库（`go list -deps` 可验证）。
