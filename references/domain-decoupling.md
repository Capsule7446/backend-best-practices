# Domain / Read Decoupling

## 基本边界

- Domain Model 负责业务行为、不变量和写侧一致性。
- Read Model 负责展示、查询、统计、搜索和报表。
- Read Model 可以冗余和反范式化，但必须可追溯 source of truth。
- Read Model 不能反向成为业务写入入口。

## 常见污染字段

- `displayStatus`、`formattedAddress`、`dashboardTotal`。
- 只为列表排序存在的派生字段。
- 只为报表统计存在的聚合字段。
- 只为前端布局存在的组合字段。

## Entity-backed API 迁移

1. 为 API 建专用 Response DTO。
2. 把查询逻辑移入 Query Service。
3. 为复杂聚合引入 DB View、Materialized View 或 Read Table。
4. 双跑新旧响应并做 parity diff。
5. 删除 Domain 中的展示字段。

## 审查问题

- 这个字段是否参与写侧不变量？
- 没有页面时它还应存在于 Aggregate 吗？
- 它是否可以从真源推导？
- 它是否需要独立刷新或容忍旧数据？
