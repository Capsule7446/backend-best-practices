# Python 语言剖面

> 供 `backend-best-practices:ddd-port-scaffold` / `backend-best-practices:ddd-adapter-impl` 及 Application/读侧相关 skill 使用。索引与未收录语言问卷见 [../language-profiles.md](../language-profiles.md)。

## Domain（领域内核）

| 中立构造 | Python 惯用法 |
| :--- | :--- |
| 端口/接口 | `Protocol`（结构子类型）/ `ABC` |
| 聚合根/实体 | `class` + 行为方法，方法内部强制不变量 |
| 值对象 | `@dataclass(frozen=True)` |
| 不可变性 | `frozen=True` |
| 按值相等 | `dataclass` 自动 `__eq__` |
| 标识（ID）类型 | `NewType('OrderId', UUID)` 或 frozen dataclass 包装 |
| 领域事件 | frozen dataclass |
| 拒绝非法操作 | 抛领域异常；Result 风格可用 `returns` 库 |
| 空值/缺失 | `T \| None`（3.10+）/ `Optional[T]` |
| 仓储接口位置 | 领域包 |

- 非法状态不可构造：校验放 `__post_init__` / 类方法工厂（`Order.place(...)`），非法即抛领域异常。
- 错误翻译为领域语义错误（`OrderAlreadyConfirmed`），不外泄 `SQLAlchemyError`/`None` 歧义。

端口骨架（中立契约 `OrderRepository`）：

```python
class OrderRepository(Protocol):
    def find_by_id(self, id: OrderId) -> Order | None: ...  # 单聚合查询
    def save(self, order: Order) -> None: ...               # 1 聚合/1 事务
```

> 契约语义（单聚合查询、1 聚合/1 事务、不变量编号）以注释/docstring 随骨架保留，不随语言丢失。

## Application（应用层）

| 关注点 | 惯用形状 |
| :--- | :--- |
| Command/Query Handler | 每用例一个类，单方法 `handle(cmd)`；或函数 + handler 注册表（简单消息总线式） |
| Unit of Work / 事务边界 | 上下文管理器式 UoW：`with uow:` 包装 SQLAlchemy `Session`，`uow.commit()` 显式提交；1 用例 = 1 事务 |
| Result/错误映射 | 领域异常在应用层翻译为用例级错误；`returns` 库的 `Result` 可选 |
| 异步语义 | asyncio `async/await`（FastAPI 栈）或同步（Flask/Celery 栈）——选一种贯穿，不要混用 |
| 幂等执行器 | 幂等键表 + 唯一约束，与业务写同一事务（同一 Session）；定义为应用层端口，实现放基础设施 |

## Read（读侧）

| 关注点 | 惯用构造 |
| :--- | :--- |
| View DTO / 投影 | frozen dataclass 或 pydantic 模型 |
| 查询侧映射 | SQLAlchemy Core `select()` 直投影 / 原生 SQL 映射到 DTO；绕过聚合与 ORM 关系加载 |

## Inbound Adapter（入站适配器）

| 入口 | 映射到 Input Port |
| :--- | :--- |
| HTTP | FastAPI router / Flask view：pydantic 校验请求 → Command → 调 Input Port |
| 消息 | aiokafka / pika consumer：反序列化 + 校验 → 调 Input Port |
| Job | Celery / Dramatiq task：payload → Command → 调 Input Port |

## Outbound Adapter（出站适配器）

| 关注点 | 惯用表达 |
| :--- | :--- |
| 仓储实现 | 基础设施包内类实现 `Protocol`（SQLAlchemy）；领域模型↔表模型显式映射（imperative mapping 可保领域类纯净） |
| Outbox | 与聚合写同事务写 outbox 表 + Celery beat / 定时任务投递 |
| 外部网关 ACL | Gateway 类 + httpx；外部响应先过 pydantic 校验再翻译成领域类型 |

## Composition Root（组合根）

- `bootstrap.py` 手工装配是惯用做法：构造适配器 → 注入 handler；`dependency-injector` 容器可选。
- FastAPI `Depends` 只用于入站边缘取已装配对象，不当全局 DI 用；领域包零框架 import。

## 架构测试

| 工具 | 用途 |
| :--- | :--- |
| import-linter | layers/forbidden contract 强制依赖方向：domain 不 import application/infrastructure |
| deptry | 依赖健康检查：未声明/未使用的第三方依赖 |

## 测试框架与包可见性

- 测试：pytest（+ pytest-asyncio）；集成测试用 Testcontainers for Python。
- 保护领域内核：语言无强制私有——`_` 前缀与 `__all__` 约定收紧公共面；依赖方向靠 import-linter 在 CI 强制，领域包保持零第三方 import。
