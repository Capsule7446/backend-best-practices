# Code Survey — 走查示例

> 附加文件，按需读取。

```text
输入：单体订单系统 src/order-monolith，目标=拆分出履约与计费。

现状领域模型（诚实版）：
  上帝类 OrderService（3000+ 行）同时做下单/扣库存/计费/开票/发货/退款。
  Order 表 30+ 列混了下单/支付状态/物流单号/发票抬头；贫血 Order 只有 getter/setter。

隐含上下文：
  | 销售/下单 | createOrder、价格快照 | 中 |
  | 履约 | shipOrder、物流单号、库存扣减 | 高（混在 OrderService）|
  | 计费 | charge、invoice、refund、发票字段 | 高 |
  同名异义: Order.status 履约语境=物流状态，计费语境=支付状态，塞进同一字段。

业务规则打捞：
  | 已发货订单不可改收货地址 | updateAddress() 第 1200 行 if | INV-A |
  | 已开票不可取消只能退款 | 散落 cancel()/refund() | INV-B |

行为黑盒：退款分账（涉第三方支付回调）尚未完全看懂 -> 标记需特征化测试。
```
