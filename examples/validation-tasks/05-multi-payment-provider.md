# 任务 05：多支付供应商

入口：`/backend-best-practices:design-pattern`

## 任务输入

> 我们的结算模块目前硬编码接入了 Stripe。本季度已签约要再接 Adyen 和本地银行网关（三家 API 形状完全不同：认证方式、金额单位、回调语义都不一样），明年还计划按国家路由到不同供应商。现在每加一个判断就要改核心结算类。目标语言 Go。

## 判据（评审人持有，勿交给执行方）

### 应出现

| 判据 | 核对位置 |
| :-- | :-- |
| `decision=use`，变化轴有真实证据（已签约的 Adyen/银行网关 = 已承诺变化，非臆测）| fit 工件 structured_summary |
| 识别出两条正交关注点：外部 API 形状差异 → Adapter/ACL；供应商选择/路由 → Strategy（或等价组合）| fit + 蓝图 |
| 稳定边界清晰：结算核心依赖统一 PaymentProvider 端口，新增供应商不改核心 | 蓝图 stable_boundary |
| `owner_layer=adapter`（网关适配）标注正确 | 蓝图 structured_summary |
| 测试义务含"新增一个供应商，核心零改动"的扩展性验证 | 蓝图 test_obligations |
| Go 惯用实现（接口 + 组合，不是 Java 类继承翻译）| 实现说明 |

### 不应出现

| 判据 | 核对位置 |
| :-- | :-- |
| 抽象工厂/桥接等超出变化轴的额外模式堆叠 | fit（auxiliary 需有独立职责理由）|
| 用 if/switch 继续堆分支当作最终方案（真实变化轴已存在）| 蓝图 |
| 隐藏控制流的过度封装（回调语义差异被抹平不可见）| review 工件 |
