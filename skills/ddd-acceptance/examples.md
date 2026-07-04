# Acceptance — 走查示例

> 附加文件，按需读取。

```text
不变量测试（INV-1 防双占）：
  正例: 空闲 slot -> Reserve 成功，发 SlotReserved
  反例: 已占 slot -> Reserve 返回 ErrSlotConflict，占用集合不变
  并发: 两 goroutine 同时 Reserve 同一 slot -> 恰一个成功

端口契约测试（RoomScheduleRepository，实现无关）：
  - save 后 findByRoom 取回等价聚合（往返一致）
  - 并发 save 旧版本 -> ConcurrencyError
  套用对象: 内存实现 + Pg 实现 都必须通过同一套契约测试

最终一致验收: 注入"占用成功但 Booking 落库失败" -> 补偿释放 slot，系统收敛 -> PASS
架构依赖测试: 断言 domain 包导入图不含 infrastructure/* -> PASS
验收报告: INV-1/2/3 全覆盖通过；AC 全通过 -> 可交付 / 可切流量。
```
