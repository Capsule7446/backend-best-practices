# 走查示例：设计态审查（节选）

输入：Ordering 上下文用例目录（4 个写用例、2 个查询用例）+ 编排设计。

检查项证据表（节选）：

| 维度 | 检查项 | 适用 | 满足 | 证据 |
| :-- | :-- | --: | --: | :-- |
| 用例完整性 | 写命令↔UC 唯一映射 | 4 | 4 | use-cases 工件 §UC 目录 |
| 用例完整性 | 追踪链完整 | 4 | 3 | UC-ORDERING-REFUND 缺 AC 编号 |
| 编排 | 状态变更委派聚合 | 4 | 3 | UC-…-CLOSE 编排 step5 写 `set status=closed` |
| 可靠性 | 幂等覆盖崩溃窗口 | 3 | 2 | UC-…-REFUND 幂等 reserve 在事务外且无 lease |
| 授权 | tenant 约束 | 6 | 6 | 各 UC authorization.application |

分级发现（节选）：

| severity | area | problem | evidence | recommendation |
| :-- | :-- | :-- | :-- | :-- |
| high | 编排 | 直接改实体状态而非委派聚合方法 | UC-…-CLOSE step5 | 改为 `Order.close()`，规则入聚合 |
| high | 可靠性 | 幂等崩溃窗口未覆盖 | UC-…-REFUND idempotency | 完成记录改与业务提交同 UoW |
| medium | 用例完整性 | 追踪链缺 AC | UC-ORDERING-REFUND | 补验收准则编号 |

硬约束触发：无。

结论：8 维中 6 维全满足；编排委派与幂等崩溃窗口各有 1 处高危缺口，均有明确修复方向。
