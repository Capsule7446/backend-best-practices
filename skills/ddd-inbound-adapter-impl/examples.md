# Inbound Adapter Impl — 走查示例

> 附加文件，按需读取。业务：取消订单。仅示意产物形状，非完整代码。

## 输入（节选）

```text
入口清单: DELETE /orders/{id}（http）；order-cancel-requests（消息主题）
用例契约: Input Port CancelOrder
  command: { order_id, reason, idempotency_key }
  errors:  [Unauthorized, NotFound, AlreadyShipped, ConcurrencyConflict, IdempotencyConflict]
语言剖面: go
```

## 产出走查：HTTP Controller

```go
func (c *OrderController) Cancel(w ResponseWriter, r *Request) {
    actor, err := c.authn.Authenticate(r)        // 认证在此层（授权不在）
    if err != nil { respond(w, 401); return }
    body, err := parseCancelRequest(r)           // 协议解析 + 格式校验
    if err != nil { respond(w, 400, problem(err)); return } // 格式非法此层拒
    result, err := c.cancelOrder.Handle(ctx(actor), CancelOrder{
        OrderID: body.OrderID, Reason: body.Reason,
        IdempotencyKey: r.Header.Get("Idempotency-Key"),
    })                                           // 唯一通道：Input Port
    if err != nil { respond(w, mapToHTTP(err)); return }
    respond(w, 200, toResponse(result))
}
// 全程无仓储、无 order.status 判断 —— 只翻译
```

## 协议级错误映射表（节选）

| 具名应用错误 | HTTP | 消息 Consumer |
| :--- | :--- | :--- |
| Unauthorized | 401/403 | 死信（不重试） |
| NotFound | 404 | 死信（不重试） |
| AlreadyShipped | 409 | ACK（业务终态，不重试） |
| ConcurrencyConflict | 409 + 重试提示 | NACK 重试 |
| IdempotencyConflict | 422 | 死信 |

## Consumer 去重钩子

```text
幂等键提取：message.headers["message-id"] → cmd.IdempotencyKey
重复投递 → 用例幂等查取命中，返回既有结果，Consumer ACK
```

## 薄度核对结果

```text
inbound 包 import 核对：仅 Input Port + DTO + 协议库；无 repository/domain 引用 → 通过
```
