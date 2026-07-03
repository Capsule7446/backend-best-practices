# Contexts — 走查示例

> 附加文件，按需读取。

```text
输入：核心域«预订与冲突» + 子域 [审批][通知][身份]。

上下文目录：
  | Scheduling 排期 | 预订与冲突 | core | 时段占用、冲突检测、预订生命周期 | 预订组 |
  | Approval 审批 | 审批 | supporting | 高价值房审批流与规则 | 预订组 |
  | Notification 通知 | 通知 | generic | 多渠道消息推送 | 平台组 |
  | Identity 身份 | 身份 | generic | 员工身份与角色（接 LDAP）| 平台组 |

词汇表（节选）：
  Scheduling.预订(Booking)：对某会议室某时段的占用主张，有生命周期。
  Approval.预订(BookingRef)：仅一个待审批对象的引用 ID + 摘要，不含排期细节。
  ⚠ 同名异义：Scheduling 的"预订"是完整聚合，Approval 只认它的引用。

边界 ADR-01：为什么 Scheduling 与 Approval 分开
  背景：审批规则常变、只作用于部分房间。
  决策：拆两个上下文，Approval 通过事件订阅 Scheduling。
  被否：合并进 Scheduling —— 会让冲突检测核心模型被审批规则污染。
```
