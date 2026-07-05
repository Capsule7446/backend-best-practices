# Read Model Sync Strategies

## query-time composition

请求时实时组合数据。适合小项目和低成本查询；不需要同步链路，但复杂查询可能影响延迟。

## synchronous application update

应用写入成功后同步更新读模型。适合同进程、同库、低复杂度场景；失败处理要明确。

## same transaction update

写模型和读表在同一事务内更新。适合单体同库且强读后写体验；注意不要让读表成为写侧规则来源。

## database view

由数据库查询定义投影。适合稳定 join；刷新实时但性能依赖数据库。

## materialized view refresh

预计算并按计划或按需刷新。适合 dashboard 和报表；必须暴露 `generatedAt` 或等价元数据。

## scheduled job

由任务定期重建/增量更新。适合可容忍延迟的报表；需要重试和补偿策略。

## CDC

从数据库变更流更新读模型。适合已有 CDC 基础设施；运维复杂度较高。

## message queue

通过消息异步投影读模型。适合跨服务和削峰；需要幂等、重试、死信和重建。

## outbox/inbox

可靠投递策略，不是 CQRS 默认要求。只有当跨服务一致性和投递可靠性值得额外复杂度时使用。

## manual rebuild

人工或运维触发重建。适合搜索索引、报表表、灾备修复；需要可重复脚本和进度记录。
