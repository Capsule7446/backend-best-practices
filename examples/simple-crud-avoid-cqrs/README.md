# simple-crud-avoid-cqrs

## 场景

用户资料 CRUD：读写字段一致，无复杂展示、报表、搜索或跨聚合查询。

## 期望

```yaml
decision: avoid
minimal_approach: dto
not_recommended:
  - event_sourcing
  - read_table
  - message_queue
reason: 普通 CRUD + Response DTO 足够，独立 Read Model 会增加无收益复杂度。
```
