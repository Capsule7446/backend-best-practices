# 任务 01：简单 CRUD（个人书签管理）

入口：`backend-best-practices:workflow-greenfield`

## 任务输入

> 我想做一个个人书签管理工具：用户注册登录后，可以新增、编辑、删除、查看自己的书签（标题、URL、可选备注、多个标签），列表页支持按标签筛选和按添加时间排序。单体小应用，用户量小，无外部系统集成，无报表需求。落地语言 TypeScript。

## 判据（评审人持有，勿交给执行方）

### 应出现

| 判据 | 核对位置 |
| :-- | :-- |
| 每个写命令（新增/编辑/删除书签）有唯一 UC 与 Input Port | use-cases 工件 |
| 列表/详情查询有视图契约（字段、筛选、排序、owner 权限）| views 工件 |
| 查询走 View DTO / Query Service，未直接暴露领域实体 | read-fit + 实现工件 |
| 归属为 Domain 不变量：owner 不可被篡改/替换，聚合方法以传入的 owner 校验操作资格（绕过 Handler 亦不可产生非法状态，对应 rubric H5）| aggregates |
| "当前调用者能否操作该书签"的访问控制在 Application 用例授权执行（身份来自可信安全上下文）——领域规则与访问控制两者分置且都存在，缺一即 fail | use-cases 授权分层表 |
| 单一 bounded context（或明确说明为何拆分）| contexts 工件 |

### 不应出现

| 判据 | 核对位置 |
| :-- | :-- |
| 独立 Read Model / Projection / 读写分离存储（fit 矩阵应全 `avoid`）| read-fit 工件 |
| Process Manager / Saga | process-managers 工件（应无或 decision=none）|
| GoF 设计模式（scan `concerns` 应为空）| patterns/01-scan.md |
| Outbox / 消息中间件作为必选项（无跨边界可靠投递需求）| orchestration 工件 |
| 微服务 / 双库 / 事件溯源 | 全部工件 |
