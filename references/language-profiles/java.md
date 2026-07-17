# Java 语言剖面

> 供 `backend-best-practices:ddd-port-scaffold` / `backend-best-practices:ddd-adapter-impl` 及 Application/读侧相关 skill 使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | Java 惯用法 |
| :--- | :--- |
| 端口/接口 | `interface` |
| 聚合根/实体 | `class` + 行为方法，方法内部强制不变量 |
| 值对象 | `record` |
| 不可变性 | `final` 字段（`record` 自动） |
| 按值相等 | `record` 自动；普通类手写 `equals/hashCode` |
| 标识（ID）类型 | 包装 `record`（`record OrderId(UUID value)`） |
| 领域事件 | 不可变 `record` |
| 拒绝非法操作 | 抛领域异常（`DomainException` 子类） |
| 空值/缺失 | `Optional<T>` |
| 仓储接口位置 | 领域包 |

- 非法状态不可构造：校验放构造器/静态工厂（`Order.place(...)`），非法即抛领域异常。
- 错误翻译为领域语义错误（`OrderAlreadyConfirmed`），不外泄 `SQLException`/`null`。

端口骨架（中立契约 `OrderRepository`）：

```java
interface OrderRepository {
    Optional<Order> findById(OrderId id); // 单聚合查询
    void save(Order order);               // 1 聚合/1 事务
}
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释随骨架保留，不随语言丢失。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | 每用例一个应用服务类，单公共方法 `handle(ConfirmOrderCommand)`；实现 Input Port 接口 |
| Unit of Work / 事务边界 | `@Transactional` 落在 handler 方法（Spring）或 `TransactionTemplate` 手工控制；1 用例 = 1 事务 |
| Result/错误映射 | 领域异常在应用层捕获并翻译为用例错误；偏函数式风格可用 vavr `Either`/`Try` |
| 异步语义 | 同步为主；异步用 `CompletableFuture`，JDK 21+ 虚拟线程可保持阻塞式写法 |
| 幂等执行器 | 幂等键表 + 唯一约束，与业务写同一事务；定义为应用层端口，实现放基础设施 |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | `record` 定义 View DTO |
| 查询侧映射 | Spring Data 接口投影 / jOOQ 映射到 record / MyBatis resultMap；直查绕过聚合 |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | Spring MVC `@RestController`：请求 DTO → Command → 调 Input Port |
| 消息 | Spring Kafka `@KafkaListener` / JMS Listener：反序列化 → 调 Input Port |
| Job | Spring `@Scheduled` / Quartz：组 Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | 基础设施包 `JpaOrderRepository implements OrderRepository`；领域模型↔持久化模型显式映射，禁止把 DB 行当聚合 |
| Outbox | 与聚合写同事务插 outbox 表 + 独立 poller 投递；重量级方案用 Debezium CDC |
| 外部网关 ACL | Gateway 类封装 `HttpClient`/OpenFeign；外部 DTO 翻译成领域语言后才越过边界 |

## Composition Root（组合根）

- Spring：`@Configuration` + `@Bean` 显式装配（优先于全量组件扫描）；无框架则在 `main` 手工 new 并构造器注入。
- 领域包不出现框架注解；`@Transactional` 若落在应用层，作为显式约定的例外。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| ArchUnit | 断言依赖方向：domain 不依赖 application/infrastructure；端口实现只在基础设施包 |
| Spring Modulith | Spring 项目的模块边界校验 |

## 测试框架与包可见性

- 测试：JUnit 5 + AssertJ + Mockito；集成测试用 Testcontainers。
- 保护领域内核：Maven/Gradle 多模块——`domain` 模块零外部依赖（编译期强制）；包私有（默认可见性）收紧构造入口；JPMS `module-info.java` 只导出领域 API。
