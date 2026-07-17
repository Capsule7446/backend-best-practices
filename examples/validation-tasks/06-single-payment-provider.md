# 任务 06：单支付供应商（反向任务）

入口：`/backend-best-practices:design-pattern`

## 任务输入

> 我们是个两人团队的小 SaaS，刚接完 Stripe 支付，能跑。我在想是不是应该现在就套上策略模式加抽象工厂，把支付层做成可插拔的，万一以后要换支付商呢？目标语言 TypeScript。

## 判据（评审人持有，勿交给执行方）

### 应出现

| 判据 | 核对位置 |
| :-- | :-- |
| `decision=simplify` 或 `avoid`（"万一以后"不是证据，无已承诺变化）| fit 工件 structured_summary |
| 给出 `simpler_alternative`：薄封装/单一模块边界隔离 Stripe SDK（一个函数级接缝即可），不建模式结构 | fit 工件 |
| 明确指出何时应当回来升级（触发条件：第二家供应商签约/明确排期）| fit 正文 |
| 流程在 fit 后结案，无蓝图/实现工件 | 工作区文件清单 |

### 不应出现

| 判据 | 核对位置 |
| :-- | :-- |
| `decision=use` 或任何 GoF 模式蓝图 | fit + 工作区 |
| 以"架构整洁/未来扩展性"作为 use 的驱动 | fit drivers |
| 借势建议 CQRS/微服务等无关升级 | 全部工件 |
