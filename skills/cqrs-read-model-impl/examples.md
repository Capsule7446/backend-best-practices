# Read Model Impl — 走查示例

> 附加文件，按需读取。仅示意结构，非完整代码。

```sql
-- 读存储结构（Read Table）：订单列表读模型
CREATE TABLE order_list_view (
  order_id           UUID PRIMARY KEY,
  tenant_id          UUID NOT NULL,          -- 权限下推的租户列
  customer_name      TEXT NOT NULL,          -- 冗余字段，投影时自真源写入
  total_amount       NUMERIC NOT NULL,
  status             TEXT NOT NULL,
  placed_at          TIMESTAMPTZ NOT NULL,   -- 排序键
  projection_version BIGINT NOT NULL,        -- freshness 元数据
  generated_at       TIMESTAMPTZ NOT NULL
);
-- 索引覆盖契约的筛选+排序；order_id 作分页稳定尾键
CREATE INDEX idx_olv_tenant_placed ON order_list_view (tenant_id, placed_at DESC, order_id);
```

```go
// Query Handler：权限下推 + freshness
func (h *ListOrders) Handle(q ListOrdersQuery, actor Actor) (Page[OrderListItem], error) {
    // 租户/行级约束进 SQL：WHERE tenant_id = $1 AND status = ANY($2) ...
    // 字段级：viewer 角色走列裁剪视图，DTO 无 cost 字段
    rows, total, err := h.reader.Find(actor.TenantID, q.Filters, q.Sort, q.Page)
    if err != nil { return Page[OrderListItem]{}, err }
    return Page[OrderListItem]{
        Items: toDTO(rows), Total: total,
        AsOf: h.reader.LastProjectedAt(),      // freshness 元数据
        Stale: h.reader.Lag() > h.tolerance,
    }, nil
}

// Projection Handler：幂等 + 乱序安全 + checkpoint
func (p *OrderProjection) On(e OrderEvent) error {
    if e.Version <= p.versionOf(e.OrderID) {   // 重复/乱序事件：跳过
        return nil
    }
    if err := p.upsert(e); err != nil {        // 更新读表（幂等 upsert）
        return err                             // 失败上抛走重试，不吞错
    }
    return p.checkpoint.Save(e.Sequence)       // 记消费位置
}

// 重建脚本：TRUNCATE 读表 -> checkpoint 归零 -> 从事件流重放 -> 校验后切流量
```

```text
缓存键含权限维度：cache key = "order_list:{tenant_id}:{filters_hash}:{page}"
  -> 跨租户绝不共享条目；字段级裁剪后的 DTO 才进缓存。

反例（禁止）：SELECT 全表后在内存按 tenant 过滤
  -> total 计数、分页游标、排序位次、聚合值与缓存键仍暴露他租户数据。
```
