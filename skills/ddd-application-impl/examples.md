# Application Impl — 走查示例

> 附加文件，按需读取。业务：取消订单。仅示意产物形状，非完整代码。

## 输入（节选）

```text
用例契约: UC-ORD-CANCEL_ORDER，Input Port CancelOrder
  command: { order_id, reason, idempotency_key }
  errors:  [Unauthorized, NotFound, AlreadyShipped, ConcurrencyConflict, IdempotencyConflict]
编排设计: OrderCancelled → 集成事件 order.cancelled.v1，经 Outbox 外发
语言剖面: go
```

## 产出走查：CancelOrderHandler（固定形状①—⑩）

```go
func (h *CancelOrderHandler) Handle(ctx Context, cmd CancelOrder) (Result, error) {
    if err := h.authz.CanCancel(ctx.Actor, cmd.OrderID); err != nil {
        return Result{}, ErrUnauthorized                    // ① 用例授权
    }
    if r, hit := h.idem.Claim(cmd.IdempotencyKey); hit {    // ② 幂等查取/占用
        return r, nil
    }
    uow := h.uowFactory.Begin(ctx)                          // ③ 开启 UoW
    order, err := h.orders.FindByID(ctx, cmd.OrderID)       // ④ 加载聚合
    if err != nil { return Result{}, ErrOrderNotFound }
    if err := order.Cancel(cmd.Reason); err != nil {        // ⑤ 业务判定在聚合内
        return Result{}, mapDomainError(err)                //    AlreadyShipped 原样具名上抛
    }
    if err := h.orders.Save(ctx, order, cmd.ExpectedVersion); err != nil {
        return Result{}, ErrConcurrencyConflict             // ⑥ 保存（带期望版本）
    }
    uow.AppendOutbox(toIntegrationEvents(order.Events()))   // ⑦ 领域事件→集成事件
    if err := uow.Commit(); err != nil { ... }              // ⑧ 提交
    h.idem.Store(cmd.IdempotencyKey, result)                // ⑨ 存幂等结果
    return Result{OrderID: ..., Status: ..., Version: ...}, nil // ⑩ 已确认事实
}
// 注意：Handler 全程无 if order.status == ... —— 状态判断在 Order.Cancel 内
```

## 错误映射表（节选）

| 来源 | 具名应用错误 |
| :--- | :--- |
| 聚合拒绝 AlreadyShipped | AlreadyShipped（原名透传） |
| Save 版本不符 | ConcurrencyConflict |
| 幂等键已被占用且参数不同 | IdempotencyConflict |

## 合规核对结果

```text
import 核对：仅端口接口 + domain 类型 → 通过
分支核对：全部属于技术结果/领域具名结果两类 → 通过
```
