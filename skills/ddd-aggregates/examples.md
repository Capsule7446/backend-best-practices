# Aggregates — 走查示例

> 附加文件，按需读取。

```text
输入：Scheduling 词汇表 + 策略（冲突即拒绝；高价值需审批）。

不变量表：
  | INV-1 | 同一会议室同一时段至多一个生效预订 | 房×时段 | 提交/确认时 | RoomSchedule |
  | INV-2 | 已确认预订的时段在取消前不可被改写 | 单预订 | 全生命周期 | Booking |
  | INV-3 | 高价值房未审批通过不得置为"生效" | 单预订 | 状态跃迁时 | Booking |

聚合目录：
  | Booking | Booking(实体) | Slot, BookingStatus, Attendees(值) | submit(), confirm(), cancel(), markApproved() |
  | RoomSchedule | RoomSchedule(实体) | Room(引用ID), 已占时段集合(值) | reserve(slot), release(slot) |

事务边界：一个事务只改一个 Booking 或一个 RoomSchedule。
一致性策略：
  Booking 提交 → RoomSchedule 占时段 | 最终一致 | 事件 BookingSubmitted | 补偿：占用失败则 Booking 转 Rejected
```
