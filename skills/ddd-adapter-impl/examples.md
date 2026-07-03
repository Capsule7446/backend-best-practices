# Adapter Impl — 走查示例

> 附加文件，按需读取。仅示意结构，非完整代码。

```go
// 领域核心（domain 包，零外部依赖）
// RoomSchedule.Reserve 在内部强制 INV-1
func (s *RoomSchedule) Reserve(slot Slot) (SlotReserved, error) {
    if s.isOccupied(slot) {                       // 守 INV-1
        return SlotReserved{}, ErrSlotConflict    // 中立领域错误
    }
    s.occupied = append(s.occupied, slot)
    return SlotReserved{RoomID: s.roomID, Slot: slot}, nil
}

// 基础设施（infrastructure 包）
// PgRoomScheduleRepository 实现 domain.RoomScheduleRepository
//   - 领域聚合 <-> 表行映射，不把 sql.Row 当聚合
//   - Save 单事务只写一个 RoomSchedule，乐观锁版本号

// 依赖装配（main / 应用启动层）
repo := infra.NewPgRoomScheduleRepository(db)   // 外层 new 具体实现
policy := domain.NewConflictPolicy(repo)        // 注入端口

// 依赖方向自检：domain 包 import 无 database/sql、无 net/http (OK)
```
