# 任务 02：复杂订单

入口：`/backend-best-practices:ddd-new`

## 任务输入

> 电商平台订单域：客户下单（多商品、优惠券、库存校验）、在线支付（第三方支付网关，支付结果异步回调）、超时 30 分钟未支付自动取消并释放库存、客户与客服都可在发货前取消（已支付则退款）。下单和支付高峰并发明显。运营需要"今日订单看板"（订单数、金额、状态分布，可容忍分钟级延迟）。多租户 SaaS，租户间数据严格隔离。落地语言 Java。

## 判据（评审人持有，勿交给执行方）

### 应出现

| 判据 | 核对位置 |
| :-- | :-- |
| Order 聚合 + 状态不变量（已发货不可取消等），状态迁移在聚合内强制 | aggregates 工件 |
| 每个写命令有 UC；取消/支付回调有幂等方案且覆盖崩溃窗口 | use-cases + orchestration |
| 支付网关调用在事务外或经 Outbox；存在"支付-履约"长流程决策（PM 或明确 choreography 理由）| orchestration + process-managers |
| 订单看板判 `use`（独立读模型），有字段来源、同步策略、重建、分钟级新鲜度声明 | views + read-fit + read-models + sync |
| 租户隔离出现在用例授权、查询权限下推、读模型缓存键三处 | use-cases + views + read 实现工件 |
| 并发敏感用例声明乐观锁/版本冲突语义 | orchestration 工件 |

### 不应出现

| 判据 | 核对位置 |
| :-- | :-- |
| 详情/简单列表也被判 `use`（应只有看板类是 `use`，其余 `avoid`）| read-fit 矩阵 |
| Handler 里出现业务判断（如 `if order.status == ...`）| application 实现工件 |
| 默认事件溯源 / 双库 / 微服务拆分 | 全部工件 |
| 无超时/补偿设计的长流程 | process-managers 工件 |
