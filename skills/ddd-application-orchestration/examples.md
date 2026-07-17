# 走查示例：取消订单编排

输入（节选）：用例 `UC-ORDERING-CANCEL-ORDER`（Input Port：CancelOrderUseCase；领域调用：Order.cancel；错误：CancellationRejected / ConcurrencyConflict / IdempotencyConflict）；可靠性要求：取消需通知履约上下文。

输出条目：

~~~yaml
orchestration:
  use_case_id: UC-ORDERING-CANCEL-ORDER
  steps:
    - { order: 1, action: coarse_authorization, owner: application }
    - { order: 2, action: idempotency_lookup_or_reserve, owner: application }
    - { order: 3, action: begin_unit_of_work, owner: application }
    - { order: 4, action: load_order, owner: application, port: OrderRepository }
    - { order: 5, action: cancel_order, owner: domain }          # Order.cancel 内部判定 INV
    - { order: 6, action: save_order, owner: application, port: OrderRepository }
    - { order: 7, action: append_integration_events, owner: application, port: OutboxPort }
    - { order: 8, action: commit_unit_of_work, owner: application }
    - { order: 9, action: store_idempotent_result, owner: application }
    - { order: 10, action: map_result, owner: application }
  transaction:
    aggregate_instances_modified: 1
    optimistic_lock: true
    rollback_on: [ domain_rejection, persistence_error, outbox_append_error ]
  idempotency:
    required: true
    scope: [ tenant_id, actor_id, use_case_id, idempotency_key ]
    same_key_different_payload: reject
    completed_request: return_previous_result
    crash_window_strategy: same_uow    # 幂等完成记录与订单保存同库同事务
  events:
    reliable_delivery_required: true
    strategy: transactional_outbox
  retry:
    allowed_for: [ transient_persistence_error ]
    forbidden_for: [ domain_rejection, authorization_failure, idempotency_conflict ]
  observability: { correlation_id: required, causation_id: required_for_events, audit: required }
~~~

反例（编排里不允许出现）：

```text
if order.status == SHIPPED: return error      # 业务判断 → 属于 Order.cancel
order.status = CANCELLED                      # 直接改实体状态 → 属于聚合方法
调用物流 API 后再 commit                        # 外部 I/O 进了事务 → 走 Outbox
```
