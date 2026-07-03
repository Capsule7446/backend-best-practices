# Domain Interactions — 走查示例

> 附加文件，按需读取。

```text
输入：Booking / RoomSchedule 聚合 + 一致性策略（最终一致，事件协作）。

领域事件目录：
  | BookingSubmitted | {bookingId, roomId, slot, isHighValue} | Booking 提交时 | owner=Scheduling | 订阅=RoomSchedule, Approval |
  | SlotReserved / SlotReserveRejected | {bookingId, roomId, slot} | RoomSchedule 占用成功/失败 | owner=Scheduling | 订阅=Booking |
  | ApprovalDecided | {bookingId, approved, approver} | Approval 决议后 | owner=Approval | 订阅=Scheduling |
  注：BookingSubmitted 不含 Attendees 全量明细（订阅方不需要）。

仓储接口（领域层端口）：
  BookingRepository
    - findById(id: BookingId) -> Booking | null            [单聚合查询]
    - save(b: Booking) -> void                              [事务:1聚合/1事务; 守 INV-2,3]
  RoomScheduleRepository
    - findByRoom(roomId: RoomId) -> RoomSchedule | null     [单聚合查询]
    - save(s: RoomSchedule) -> void                         [事务:1聚合/1事务; 守 INV-1]

契约语义（节选）：
  RoomSchedule.reserve(slot) | 前置: canReserve 真 | 后置: 占用+slot, 发 SlotReserved | 失败: 已占→发 SlotReserveRejected | 守 INV-1
```
