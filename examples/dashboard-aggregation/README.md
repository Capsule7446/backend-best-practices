# dashboard-aggregation

## 场景

运营后台展示订单数、支付金额、退款率、库存预警。数据来自 Order、Payment、Refund、Inventory。

## 期望

```yaml
decision: use
minimal_approach: materialized-view
drivers:
  - 跨多个业务来源聚合
  - 查询形状不同于写模型
  - 统计指标适合预计算
sync_strategy: scheduled_job
freshness: scheduled
```
