# 走查示例：取消订单

输入（节选）：命令·事件目录含 `CancelOrder → OrderCancelled`；聚合目录含 `Order`（INV-ORDER-04 已发货不可取消、INV-ORDER-07 仅本人或客服可取消）。

输出条目：

~~~yaml
use_case:
  id: UC-ORDERING-CANCEL-ORDER
  bounded_context: Ordering
  kind: command
  actor: { type: Customer, authentication_required: true }
  trigger: { type: http, source: "POST /orders/{id}/cancel" }
  input_port: CancelOrderUseCase
  command:
    type: CancelOrderCommand
    fields:
      order_id: OrderId
      reason: CancellationReason
      expected_version: Integer?
      idempotency_key: IdempotencyKey?
  authorization:
    application: [ "actor 可发起 CancelOrder" ]
    domain: [ "订单所有权与当前状态允许取消（INV-ORDER-04/07）" ]
  domain_invocations:
    - { aggregate: Order, method: cancel, invariants: [INV-ORDER-04, INV-ORDER-07] }
  expected_events: [ OrderCancelled ]
  result:
    type: CancelOrderResult
    fields:
      order_id: OrderId
      committed_status: OrderStatus
      aggregate_version: Integer
      consistency_token: ConsistencyToken?
  errors: [ Unauthorized, OrderNotFound, CancellationRejected, ConcurrencyConflict, IdempotencyConflict ]
  acceptance: [ AC-ORDER-CANCEL-01, AC-ORDER-CANCEL-02 ]
~~~

追踪表行：`GOAL-REDUCE-DISPUTES → CMD-CANCEL-ORDER → UC-ORDERING-CANCEL-ORDER → Order.cancel → INV-ORDER-04/07 → OrderCancelled → AC-ORDER-CANCEL-01/02`

要点：

- Result 只回传本事务已确认的事实，不等待任何异步读模型。
- "能否取消"的预检查是查询用例；真正执行时 Domain 仍须重新验证。
- 排除示例：`SyncLegacyOrders` 是运维脚本、不改业务事实 → 标注排除，不建 UC。
