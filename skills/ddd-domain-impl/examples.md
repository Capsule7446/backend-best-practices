# Domain Impl — 走查示例

> 附加文件，按需读取。业务：取消订单。仅示意产物形状，非完整代码。

## 输入（节选）

```text
接口骨架: Order 聚合，占位方法 Cancel(reason) -> Result
契约语义: INV-2 已发货(Shipped)订单不可取消，拒绝名 AlreadyShipped
          取消成功产生领域事件 OrderCancelled
语言剖面: go
```

## 产出走查

```go
// 值对象与标识（构造即校验、按值相等、不可变）
type OrderID struct{ value string }
// NewOrderID("") -> ErrEmptyOrderID —— 非法值拒于构造点

type CancelReason struct{ value string }  // 同上，构造成功即合法

// 聚合根行为：Cancel 在内部强制 INV-2
func (o *Order) Cancel(reason CancelReason) error {
    if o.status == Shipped {          // 守 INV-2
        return ErrAlreadyShipped      // 具名领域拒绝，非技术异常
    }
    o.status = Cancelled              // 状态只经根方法变更
    o.record(OrderCancelled{          // 过去式事件：登记发布点，不发送
        OrderID:  o.id,
        Reason:   reason,
        OccurredAt: o.clock(),
    })
    return nil
}
```

## 发布点登记表

| 根方法 | 事件 | 事实数据 |
| :--- | :--- | :--- |
| Order.Cancel | OrderCancelled | OrderID, Reason, OccurredAt |

## 依赖纯净性核对结果

```text
domain 包 import 核对：无 database/sql、无 net/http、无框架 → 通过
```
