# Kotlin 语言剖面

> 供 `ddd-port-scaffold` 与各分层实现能力（`ddd-domain-impl` / `ddd-application-impl` / `ddd-inbound-adapter-impl` / `ddd-outbound-adapter-impl` / `cqrs-read-model-impl`）使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | Kotlin 惯用法 |
| :--- | :--- |
| 端口/接口 | `interface` |
| 聚合根/实体 | `class` + 行为方法，方法内部强制不变量 |
| 值对象 | `data class` |
| 不可变性 | `val` |
| 按值相等 | `data class` 自动 |
| 标识（ID）类型 | `@JvmInline value class OrderId(val value: UUID)` |
| 领域事件 | `data class`（全 `val`） |
| 拒绝非法操作 | `require/check` + 领域异常，或 sealed 错误 + `Result` |
| 空值/缺失 | `T?` |
| 仓储接口位置 | 领域包 |

- 非法状态不可构造：校验放 `init {}` / 伴生对象工厂（`Order.place(...)`），非法即拒绝。
- 领域错误用 `sealed interface/class` 层级建模（`OrderAlreadyConfirmed`），不外泄底层异常。

端口骨架（中立契约 `OrderRepository`）：

```kotlin
interface OrderRepository {
    fun findById(id: OrderId): Order? // 单聚合查询
    fun save(order: Order)            // 1 聚合/1 事务
}
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释随骨架保留，不随语言丢失。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | 每用例一个类，`suspend fun handle(cmd: ConfirmOrderCommand)` 单公共方法；实现 Input Port 接口 |
| Unit of Work / 事务边界 | Spring `@Transactional`（支持 suspend）/ Exposed `transaction {}` / `newSuspendedTransaction {}`；1 用例 = 1 事务 |
| Result/错误映射 | sealed class 错误层级 + `kotlin.Result` 或 Arrow `Either`；不让领域异常裸穿到适配器 |
| 异步语义 | coroutine：`suspend` 贯穿应用层，结构化并发；`Dispatchers` 切换留在适配器层 |
| 幂等执行器 | 幂等键表 + 唯一约束，与业务写同一事务；定义为应用层端口，实现放基础设施 |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | `data class` 定义 View DTO |
| 查询侧映射 | Exposed DSL / jOOQ 直查映射到 data class；Spring Data 接口投影；绕过聚合 |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | Ktor routing / Spring `@RestController`：请求 DTO → Command → 调 Input Port |
| 消息 | Spring Kafka `@KafkaListener` / kafka-clients 消费循环：反序列化 → 调 Input Port |
| Job | Quartz / Spring `@Scheduled`：组 Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | 基础设施包内类实现领域接口（Exposed/JPA）；领域模型↔持久化模型显式映射 |
| Outbox | 与聚合写同事务插 outbox 表 + 独立 poller（coroutine 定时任务或 Quartz）投递 |
| 外部网关 ACL | Gateway 类封装 Ktor client / OpenFeign；外部 DTO 翻译成领域语言后才越过边界 |

## Composition Root（组合根）

- Koin 模块声明 / Spring DI；无框架则在 `main` 手工装配，构造器注入。
- 领域包零框架注解；`value class`/`data class` 不掺 ORM 注解，映射放适配器。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| Konsist | Kotlin 原生结构断言：分层依赖方向、命名约定 |
| ArchUnit | JVM 字节码级依赖检查（Kotlin 同样适用） |

## 测试框架与包可见性

- 测试：Kotest 或 JUnit 5 + MockK；`kotlinx-coroutines-test` 测 suspend 逻辑；集成测试用 Testcontainers。
- 保护领域内核：Gradle 多模块——`domain` 模块零外部依赖（编译期强制）；`internal` 限制模块内可见，收紧工厂/构造入口。
