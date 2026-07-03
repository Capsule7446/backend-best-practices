# Workflow：Brownfield（既有项目改造）

> 统筹者。本文件**唯一**掌握顺序、文件交接、门禁与回溯；被调用的 SKILL 都是纯能力。由 `/backend-best-practices:ddd-refactor` 触发。
> 第一纪律：**旧系统全程可运行、可回滚，绝不一次性重写。**

## 0. 入口路由（原 mode-router 职责，已并入本层）

1. **判定驱动**：有可运行代码且目标是解耦/拆分/可测试性 → brownfield（本流程）；否则转 `workflow-greenfield`。
2. **采集最小上下文**：代码库可访问路径；改造目标；不可中断的运行约束。
3. **拆切片**：把改造目标拆成可独立推进的切片。
4. **登记语言**：缺省沿用现有技术栈。
5. **建运行工作区** `<workdir>/`，写 `00-routing.md` 与 `_manifest.md`。

## 1. 前段：逆向与规划（brownfield 独有）

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 00 | （路由，本层）| 代码库 + 改造目标 | `00-routing.md` | |
| 01 | ddd-code-survey | `00-routing.md` + 代码库 | `01-survey.md` | **G0** |
| 02 | ddd-seam-finder | `01-survey.md` | `02-seams.md` | |
| 03 | ddd-strangler-plan | `02-seams.md`,`01-survey.md` | `03-plan.md` | **G1** |

## 2. 后段：逐切片循环（与 greenfield 汇流复用同一批纯能力）

`03-plan.md` 的切片顺序驱动循环。**每个切片 `<slice>` 用独立子工作区** `<workdir>/<slice>/`：

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| s0 | （补特征化测试，本层）| `03-plan.md` 的该片测试范围 + 行为黑盒 | `<slice>/00-characterization.md` | **G2** |
| s1 | ddd-aggregates（局部）| 该片词汇 + `01-survey.md` 规则 | `<slice>/01-aggregates.md` | |
| s2 | ddd-domain-interactions | `<slice>/01-aggregates.md` | `<slice>/02-interactions.md` | |
| s3 | ddd-model-review | `<slice>/01..02` | `<slice>/03-review.md` | 复用 greenfield G2 |
| s4 | ddd-spec-bridge | `<slice>/01..02` | `<slice>/04-spec.md` | |
| s5 | ddd-port-scaffold | `<slice>/04-spec.md` + 剖面 | `<slice>/05-ports.md` | 复用 greenfield G3 |
| s6 | ddd-adapter-impl | `<slice>/05-ports.md`,`04-spec.md` | `<slice>/06-impl.md` | |
| s7 | ddd-acceptance | `<slice>/04-spec.md`,`06-impl.md`,`00-characterization.md` | `<slice>/07-acceptance.md` | **G3** |
| s8 | （流量切换+验收，本层）| `<slice>/07-acceptance.md` | 更新 `_manifest.md` | |

切片验收通过并切流量稳定后取下一片。

## 3. 门禁（读产物文件核对）

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 现状 | `01-survey.md` 后 | 现状模型可解释现有关键行为；坏味道与行为黑盒已列清 |
| G1 规划 | `03-plan.md` 后 | 切片顺序、回滚策略、特征化测试范围获确认；满足"旧系统始终可运行" |
| G2 切片安全 | 每片落地前（`<slice>/00-characterization.md`）| 特征化测试已覆盖该片现有行为（无裸切）|
| G3 切片验收 | 每片 `<slice>/07-acceptance.md` 后 | 通过契约/不变量测试；行为与旧实现等价；可切流量且可回滚 |

## 4. 回溯矩阵（本层独有）

| 触发条件 | 重跑 |
| :-- | :-- |
| 该重写而非改造（核心不可救）| 回到路由重新分流/重定目标 |
| 改造目标在代码现实下不成立 | 回到路由与用户重定目标 |
| 现状模型不足以定位接缝 | ddd-code-survey |
| ACL 翻不动旧模型（结构冲突）| ddd-code-survey |
| 切片无法解耦/独立交付 | ddd-seam-finder |
| 特征化测试覆盖不了旧行为 | ddd-code-survey |
| 切片边界与聚合边界冲突 | ddd-strangler-plan（重排切片）|
| 新旧行为不等价（非预期）| ddd-code-survey |
| 端口契约语言无法表达 | ddd-spec-bridge |

> 进入局部战术建模后，`workflow-greenfield` §3 回溯矩阵中与 aggregates/interactions/review/spec 相关的条目同样适用。

## 5. 编排纪律

- **一次只动一片**：完成、验收、可回滚后再取下一片。
- **先兜底再替换**：没有特征化测试不动实现（G2 是硬门禁）。
- **沿用现有语言**：除非明确换栈，取现有技术栈对应语言剖面。
- **ACL 是临时的**：按 `03-plan.md` 的退役计划下线临时 ACL 与旧字段。
- **绞杀者纪律**：旧路径全程可用、可回滚，新实现灰度接管。
