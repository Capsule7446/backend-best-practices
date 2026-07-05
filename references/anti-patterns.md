# CQRS Read Model Anti-patterns

- 只有文件夹叫 `command/query`，但模型没有真正分离。
- 读 API 直接返回 Domain Entity。
- Aggregate 为页面展示加入统计、格式化、排序字段。
- Read Model 字段没有 source of truth。
- Read Model 没有刷新策略。
- 所有 CRUD 都强行套 CQRS。
- 默认 Event Sourcing。
- 默认微服务。
- 默认双库。
- Read Model 变成业务真源。
- 隐藏 stale data，不告诉用户数据生成时间。
- 为普通分页默认引入搜索引擎。
- 为小型单体默认引入 Outbox/Inbox。
