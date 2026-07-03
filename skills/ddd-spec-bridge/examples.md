# Spec Bridge — 走查示例

> 附加文件，按需读取。

```text
== 端口契约规范 v1.0（上下文：Scheduling，纯中立）==

Port: BookingRepository  [聚合: Booking]
  - findById(id: BookingId) -> Booking | null      查询边界: 单聚合; 失败: 不存在返回 null
  - save(booking: Booking) -> void                 事务: 1 聚合/1 事务; 守 INV-2,3; 失败: 乐观锁冲突抛 ConcurrencyError

Port: ConflictPolicy  [领域服务]
  - canReserve(roomId: RoomId, slot: Slot) -> Boolean   前置: slot.start<end; 后置: 无副作用; 守 INV-1

== 领域事件 schema ==
  BookingSubmitted  v1  owner=Scheduling  兼容=加字段向后兼容
    { bookingId: BookingId, roomId: RoomId, slot: Slot, isHighValue: Boolean }

== 不变量命题集 ==
  INV-1: 当 (roomId, slot) 已存在生效占用时，任何新的 reserve(同 slot) 必须失败。

== 验收准则 ==
  AC-1 (INV-1): Given 09:00-10:00 已被 B1 占；When B2 尝试占同段；Then reserve 失败并产生 SlotReserveRejected，B1 不变。
```
