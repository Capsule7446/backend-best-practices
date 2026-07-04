# Port Scaffold — 走查示例

> 附加文件，按需读取。语言剖面完整映射见插件根 `references/language-profiles.md`。

```text
输入端口契约（节选）+ 语言剖面 go：
  Port: BookingRepository
    - findById(id: BookingId) -> Booking | null   [单聚合查询]
    - save(b: Booking) -> void                     [1 聚合/1 事务]
  Invariant INV-3: 已确认的预订不可修改时段

→ 产出 Go 骨架：
  type BookingRepository interface {
      // FindById 单聚合查询边界
      FindById(ctx context.Context, id BookingID) (*Booking, error)
      // Save 事务边界：1 聚合/1 事务；维护 INV-3
      Save(ctx context.Context, b *Booking) error
  }
  // BookingID 值对象：按值相等
  type BookingID struct{ value string }
  // …实现留给 adapter-impl
```
