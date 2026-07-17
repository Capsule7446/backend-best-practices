# TypeScript 语言剖面

> 供 `ddd-port-scaffold` 与各分层实现能力（`ddd-domain-impl` / `ddd-application-impl` / `ddd-inbound-adapter-impl` / `ddd-outbound-adapter-impl` / `cqrs-read-model-impl`）使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | TypeScript 惯用法 |
| :--- | :--- |
| 端口/接口 | `interface` |
| 聚合根/实体 | `class` + 行为方法，方法内部强制不变量 |
| 值对象 | `readonly` 类型 / `Object.freeze` |
| 不可变性 | `readonly` 字段与 `Readonly<T>` |
| 按值相等 | 手写 `equals()` 或结构比较 |
| 标识（ID）类型 | branded type（`type OrderId = string & { readonly __brand: 'OrderId' }`） |
| 领域事件 | `readonly` 类型（不可变对象字面量或类） |
| 拒绝非法操作 | 抛领域错误类，或返回 `Result<T, E>` 判别联合 |
| 空值/缺失 | `T \| null`（`strictNullChecks` 开启） |
| 仓储接口位置 | 领域模块（只导出接口与领域类型） |

- 非法状态不可构造：私有构造器 + 静态工厂（`Order.place(...)` 返回 `Result`），非法即拒绝。
- 错误翻译为领域语义错误（`OrderAlreadyConfirmed`），不外泄 ORM 异常/`undefined`。

端口骨架（中立契约 `OrderRepository`）：

```typescript
interface OrderRepository {
    findById(id: OrderId): Promise<Order | null>; // 单聚合查询
    save(order: Order): Promise<void>;            // 1 聚合/1 事务
}
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释随骨架保留，不随语言丢失。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | 每用例一个类，单方法 `execute(cmd): Promise<Result<T, E>>`；或闭包工厂函数注入端口 |
| Unit of Work / 事务边界 | ORM 事务回调：Prisma `$transaction(async tx => ...)` / Kysely `transaction().execute()` / TypeORM QueryRunner；事务句柄传给仓储；1 用例 = 1 事务 |
| Result/错误映射 | neverthrow `Result` 或手写判别联合；领域错误在适配器边缘映射 HTTP 状态 |
| 异步语义 | 全链路 `Promise`/`async-await`；取消用 `AbortSignal` 约定透传 |
| 幂等执行器 | 幂等键表 + 唯一约束，与业务写同一事务；定义为应用层端口，实现放基础设施 |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | 纯 `interface`/`type` DTO |
| 查询侧映射 | Kysely / Prisma `select` 只取所需列直投影；出口可用 zod schema 校验形状；绕过聚合 |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | Fastify/Express route / NestJS controller：zod 校验请求 → Command → 调 Input Port |
| 消息 | kafkajs consumer：反序列化 + 校验 → 调 Input Port |
| Job | BullMQ worker：job payload → Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | 基础设施目录内类实现领域接口（Prisma/Kysely/Drizzle）；领域模型↔持久化行显式映射 |
| Outbox | 与聚合写同事务写 outbox 表 + 定时 poller（BullMQ repeatable job 可承担）投递 |
| 外部网关 ACL | Gateway 类 + `fetch`/axios；外部响应先过 zod 校验再翻译成领域类型 |

## Composition Root（组合根）

- 组合根模块手工工厂装配（构造器注入），入口文件自底向上 new；NestJS 项目用 Module DI。
- 轻量容器 tsyringe / InversifyJS 可选；领域模块零框架/装饰器依赖。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| dependency-cruiser | 声明式依赖规则：禁止 domain import infrastructure，CI 报告 |
| eslint-plugin-boundaries | 分层边界 lint：按目录/别名限制 import 方向 |

## 测试框架与包可见性

- 测试：Vitest（或 Jest）；集成测试用 Testcontainers for Node.js。
- 保护领域内核：无包级可见性——目录 + `index.ts` barrel 只导出公共 API，配 eslint `no-restricted-imports` / dependency-cruiser 禁止深层 import；类内部用 `#private` 字段。
