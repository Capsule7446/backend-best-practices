# Context Map — 走查示例

> 附加文件，按需读取。

```text
输入：[Scheduling][Approval][Notification][Identity] + 跨界待解清单。

集成模式表：
  | Scheduling→Approval | 事件订阅（预订待审批）| 异步 | 最终一致 |
  | Approval→Scheduling | 事件订阅（审批结果）| 异步 | 最终一致 |
  | *→Notification | OHS+PL（通知发布语言）| 异步 | 最终一致 |
  | *→Identity | ACL 包 LDAP | 同步 | 强一致（读）|

契约所有权：
  BookingPendingApproval：owner=Scheduling，消费=Approval，向后兼容加字段
  ApprovalDecided：owner=Approval，消费=Scheduling
  NotifyMessage：owner=Notification(OHS)，消费=全体，版本化

核心保护核对：
  Scheduling(core)：对 Identity 用 ACL；对 Approval/Notification 仅发/收事件，外部概念不进核心模型。✅
```
