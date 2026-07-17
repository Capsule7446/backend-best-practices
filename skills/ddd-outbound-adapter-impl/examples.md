# Outbound Adapter Impl — 走查示例

> 附加文件，按需读取。业务：取消订单。仅示意产物形状，非完整代码。

## 输入（节选）

```text
出站端口: OrderRepository { FindByID, Save(order, expectedVersion) }
          RefundGateway { RequestRefund(orderID, amount) }
投递要求: OrderCancelled → order.cancelled.v1，经 Outbox 至少一次投递
语言剖面: go；数据库 postgres
```

## 产出走查

```go
// 仓储适配器：显式映射 + 乐观锁 + 1 聚合/1 事务
func (r *PgOrderRepository) Save(ctx Context, o *Order, expected int) error {
    row := toOrderRow(o)                      // 领域 → 行：显式映射，不把行当聚合
    res := r.tx(ctx).Exec(
        `UPDATE orders SET status=$1, version=version+1
          WHERE id=$2 AND version=$3`,        // 乐观锁：期望版本比对
        row.Status, row.ID, expected)
    if res.RowsAffected() == 0 { return ErrVersionConflict } // 具名，不吞
    return nil
}

// UoW：聚合保存 + Outbox 写入同事务
uow.Commit():  BEGIN → UPDATE orders → INSERT INTO outbox(...) → COMMIT

// Outbox 行形状
outbox(id, event_type='order.cancelled.v1', payload, occurred_at,
       delivered_at NULL, attempts)          // 投递器轮询 → 发送 → 标记，失败退避

// 外部系统网关（ACL）：外部概念止步于此
func (g *StripeRefundGateway) RequestRefund(id OrderID, amt Money) error {
    resp, err := g.client.CreateRefund(...)  // 超时/重试封在网关内
    return translateStripeError(err)          // stripe 错误码 → 领域语言，不穿透
}

// Composition Root（main）：核心零 new
orders  := pg.NewPgOrderRepository(db)
refunds := stripe.NewStripeRefundGateway(cfg)
handler := app.NewCancelOrderHandler(orders, refunds, uowFactory, idemStore)
```

## 依赖方向核对结果

```text
domain / app 包 import 核对：无 pg、无 stripe、无消息中间件 → 通过
装配清单：OrderRepository→PgOrderRepository、RefundGateway→StripeRefundGateway（均在 main）
```
