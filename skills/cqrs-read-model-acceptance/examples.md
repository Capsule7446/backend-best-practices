# Read Model Acceptance — 走查示例

> 附加文件，按需读取。

```text
查询契约测试（order_list 契约）：
  test/read/order_list_query_test.go
    - filters_by_status_and_date_range        -> PASS
    - sorts_by_placed_at_desc_by_default      -> PASS
    - paginates_last_page_and_out_of_range    -> PASS（越界返回空页 + 正确 total）
    - returns_empty_page_when_no_match        -> PASS

权限隔离（含越权负例）：
  test/read/order_list_authz_test.go
    - tenant_b_cannot_see_tenant_a_rows       -> PASS（items=0 且 total=0，游标不前进）
    - field_level_hides_cost_for_viewer_role  -> PASS（DTO 无 cost 字段）
    - aggregate_sum_excludes_other_tenants    -> PASS
    - cache_key_scoped_by_tenant              -> PASS（A 的命中不泄给 B）

投影收敛：
  test/read/projection_convergence_test.go
    - duplicate_event_applied_exactly_once    -> PASS
    - out_of_order_events_converge_by_version -> PASS
    - full_replay_equals_incremental_state    -> PASS（逐行 diff = 0）

失败处理 / 重建等价：
  test/read/projection_failure_test.go
    - retries_then_routes_to_dlq_after_3      -> PASS（DLQ 有毒消息，后续事件不阻塞）
  test/read/rebuild_equivalence_test.go
    - rebuild_from_zero_checkpoint_equals_live -> PASS（1000 行逐字段等价）

read-your-writes / 新鲜度 / 性能 / 降级：
  test/read/consistency_test.go
    - token_path_returns_own_write            -> PASS
    - stale_flag_set_when_lag_exceeds_5s      -> PASS
  test/read/query_budget_test.go
    - p95_under_200ms_at_1m_rows              -> PASS
  test/read/fallback_test.go
    - explicit_error_when_read_store_down     -> FAIL（当前静默返回空列表）

验收报告（节选）：
  | category | check          | result | evidence                                   |
  | 降级回退 | 读存储不可用   | fail   | fallback_test.go::explicit_error_when_... |
  结论：9/10 通过；降级回退 FAIL -> 阻断，修复后重跑该项。

无证据示例："字段正确性：已覆盖"（无测试文件名+用例名）-> 记为无证据，不计入通过。
```
