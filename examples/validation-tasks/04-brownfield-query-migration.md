# 任务 04：Brownfield 查询迁移

入口：`/backend-best-practices:cqrs-read-model-refactor`

## 任务输入

> 现状：一个运行 4 年的 Spring Boot 单体，`/api/orders/search` 接口直接把 JPA 的 Order Entity（含 12 个懒加载关联）序列化返回给前端，列表页要 8 秒才能打开。任何人改 Order 实体都可能弄坏这个接口。生产环境不能停机，前端不能一次性改造，要求可以随时回退。

## 判据（评审人持有，勿交给执行方）

### 应出现

| 判据 | 核对位置 |
| :-- | :-- |
| 先定位 Entity 直出与 Domain 污染（decoupling 在前）| 01-domain-read-decoupling |
| 按现状查询/页面提取视图契约，逐视图 fit（不是全局一刀切）| 02-views + 03-fit-check |
| 迁移路径含双跑对比（Shadow Read + Parity Diff）→ 灰度 Cutover → Rollback 开关；**Backfill 仅当 fit 为该视图选择独立物化读存储时要求**（同库 DB View/Query Service 方案无可回填项，不得因缺 Backfill 判失败）| migration-log 设计/工件 + fit 矩阵 |
| Parity Diff 差异归零或全部有解释才切流 | 迁移门禁 |
| 旧路径保留至稳定期后退役，退役有登记 | migration 工件 |
| 新查询出口是 View DTO，不再暴露 Entity | 实现工件 |

### 不应出现

| 判据 | 核对位置 |
| :-- | :-- |
| 一次性重写/直接替换旧接口（无双跑对比）| 迁移设计 |
| 为救急默认引入消息队列/双库（简单 Read Table/DB View 足够时）| fit + read-models |
| 没有回滚开关就切流 | 迁移门禁 |
| 借迁移顺手改业务行为（行为等价被破坏）| Parity Diff 判据 |
