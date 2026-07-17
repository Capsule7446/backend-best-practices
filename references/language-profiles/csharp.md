# C# 语言剖面

> 供 `ddd-port-scaffold` 与各分层实现能力（`ddd-domain-impl` / `ddd-application-impl` / `ddd-inbound-adapter-impl` / `ddd-outbound-adapter-impl` / `cqrs-read-model-impl`）使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | C# 惯用法 |
| :--- | :--- |
| 端口/接口 | `interface`（`I` 前缀） |
| 聚合根/实体 | `class` + 行为方法，方法内部强制不变量 |
| 值对象 | `record` / `readonly record struct` |
| 不可变性 | `init`-only 属性 / `readonly` |
| 按值相等 | `record` 自动 |
| 标识（ID）类型 | `readonly record struct OrderId(Guid Value)` |
| 领域事件 | `record` |
| 拒绝非法操作 | 抛领域异常，或 Result 类型（ErrorOr / FluentResults / 自写） |
| 空值/缺失 | `T?`（启用 nullable reference types） |
| 仓储接口位置 | 领域程序集（Domain project） |

- 非法状态不可构造：校验放私有构造器 + 静态工厂（`Order.Place(...)`），非法即拒绝。
- 错误翻译为领域语义错误（`OrderAlreadyConfirmed`），不外泄 `DbException`/`null`。

端口骨架（中立契约 `OrderRepository`）：

```csharp
interface IOrderRepository {
    Order? FindById(OrderId id); // 单聚合查询
    void Save(Order order);      // 1 聚合/1 事务
}
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释随骨架保留，不随语言丢失。实际项目常用 `Task<Order?> FindByIdAsync(..., CancellationToken ct)` 异步变体。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | MediatR `IRequestHandler<TCommand, TResult>`，或每用例一个普通应用服务类 |
| Unit of Work / 事务边界 | EF Core `DbContext` 天然是 UoW：一次 `SaveChangesAsync` = 一次提交；显式事务用 `IDbContextTransaction`；1 用例 = 1 事务 |
| Result/错误映射 | Result 模式（ErrorOr / FluentResults）或领域异常，在适配器边缘统一转 ProblemDetails |
| 异步语义 | `async/await` + `Task` 全链路；`CancellationToken` 从入口透传到出站适配器 |
| 幂等执行器 | 幂等键表 + 唯一约束，与业务写同一事务；MassTransit inbox/outbox 有现成实现 |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | `record` 定义 View DTO |
| 查询侧映射 | Dapper 直查，或 EF Core `AsNoTracking().Select(...)` 投影；不加载聚合 |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | ASP.NET Core Minimal API / Controller：请求 DTO → Command → 调 Input Port |
| 消息 | MassTransit / Azure Service Bus consumer：反序列化 → 调 Input Port |
| Job | Hangfire / Quartz.NET：组 Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | Infrastructure 程序集内类实现领域接口（EF Core）；领域模型↔持久化模型显式映射 |
| Outbox | MassTransit transactional outbox，或手写 outbox 表 + `BackgroundService` 投递 |
| 外部网关 ACL | Gateway 类 + typed `HttpClient`（`IHttpClientFactory`）；外部 DTO 翻译成领域语言后才越过边界 |

## Composition Root（组合根）

- `Microsoft.Extensions.DependencyInjection`：Program.cs 显式注册；批量注册用 Scrutor 扫描。
- 生命周期由容器管理（Scoped per request）；领域程序集不引用任何 DI/框架包。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| NetArchTest.Rules | 断言程序集/命名空间依赖方向：Domain 不依赖 Application/Infrastructure |
| ArchUnitNET | 更细粒度的架构断言（ArchUnit 的 .NET 移植） |

## 测试框架与包可见性

- 测试：xUnit + FluentAssertions + NSubstitute（或 Moq）；集成测试用 Testcontainers for .NET。
- 保护领域内核：Domain 独立程序集不引用 Infrastructure（编译期强制）；`internal` + `[InternalsVisibleTo]` 只对测试程序集开放。
