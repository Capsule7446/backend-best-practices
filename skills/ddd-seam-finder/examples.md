# Seam Finder — 走查示例

> 附加文件，按需读取。

```text
输入：订单单体现状模型（OrderService 上帝类，履约/计费混杂，Order.status 同名异义）。

接缝清单：
  | 缝1 履约边界 | 事件接缝 | 下单<->履约 | 中：扣库存当前同步，可改为 OrderPlaced 事件 |
  | 缝2 计费边界 | 接口接缝 | 下单<->计费 | 中：charge() 抽成 BillingPort 接口注入 |
  | 缝3 物流状态读 | 视图接缝 | 旧 Order 表<->新履约模型 | 易：先用读视图隔离物流字段 |

防腐层落点：
  | ACL-Fulfillment | 新履约模型<->旧 Order 表/库存 | 翻译"订单行->发货单" | 双向 |
  | ACL-Billing | 新计费模型<->旧支付回调 | 翻译第三方支付术语->领域语言 | 入站为主 |

同名异义拆分：
  Order.status -> FulfillmentStatus(履约) + PaymentStatus(计费)，ACL 在缝处双写过渡，迁移完成后下线旧字段。
```
