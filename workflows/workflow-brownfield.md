# Workflow：Brownfield（既有项目改造）

> 统筹者。本文件**唯一**掌握顺序、文件交接、门禁与回溯；被调用的 SKILL 都是纯能力。由 `/backend-best-practices:ddd-refactor` 触发。
> 第一纪律：**旧系统全程可运行、可回滚，绝不一次性重写。**

## 0. 入口路由（原 mode-router 职责，已并入本层）

1. **判定驱动**：有可运行代码且目标是解耦/拆分/可测试性 → brownfield（本流程）；否则转 `workflow-greenfield`。
2. **采集最小上下文**：代码库可访问路径；改造目标；不可中断的运行约束。
3. **拆切片**：把改造目标拆成可独立推进的切片。
4. **登记语言**：缺省沿用现有技术栈。
5. **建运行工作区** `<workdir>/`（默认 `./run/refactor/`），写 `00-routing.md` 与 `_manifest.md`。

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
| s3 | ddd-model-review | `<slice>/01..02-*.md` | `<slice>/03-review.md` | 复用 greenfield G2 |
| s4 | ddd-application-use-cases | 该片命令/入口 + `<slice>/01..02-*.md` | `<slice>/04-use-cases.md` | |
| s5 | ddd-application-orchestration | `<slice>/04-use-cases.md`,`01-aggregates.md` | `<slice>/05-orchestration.md` | |
| s6 | ddd-process-manager-design | `<slice>/05-orchestration.md`（长流程候选）| `<slice>/06-process-managers.md` | 条件执行 |
| s7 | ddd-application-review | `<slice>/04..06-*.md` | `<slice>/07-application-review.md` | 复用 greenfield G3 |
| s8 | ddd-spec-bridge | `<slice>/01..06-*.md` | `<slice>/08-spec.md` | |
| s9 | ddd-port-scaffold | `<slice>/08-spec.md` + 剖面 | `<slice>/09-scaffold.md` | 复用 greenfield G6 |
| s10 | ddd-domain-impl | `<slice>/09-scaffold.md`,`08-spec.md` | `<slice>/10-domain-impl.md` | |
| s11 | ddd-application-impl | `<slice>/09-scaffold.md`,`08-spec.md`,`05-orchestration.md` | `<slice>/11-application-impl.md` | |
| s12 | ddd-outbound-adapter-impl | `<slice>/09-scaffold.md`,`08-spec.md` | `<slice>/12-outbound-impl.md` | |
| s13 | ddd-inbound-adapter-impl | `<slice>/09-scaffold.md`,`04-use-cases.md` | `<slice>/13-inbound-impl.md` | |
| s14 | ddd-application-review | `<slice>/04..06-*.md` + `11-application-impl.md` + 测试证据 | `<slice>/14-application-review-impl.md` | 复用 greenfield G7 |
| s15 | ddd-acceptance | `<slice>/08-spec.md`,`10..13-*.md`,`00-characterization.md` | `<slice>/15-acceptance.md` | **G3** |
| s16 | （流量切换+验收，本层）| `<slice>/15-acceptance.md` | 更新 `_manifest.md` | |

切片验收通过并切流量稳定后取下一片。

读侧切片（查询/报表/API 污染类）不走 s4-s6，改走 `workflow-read-model-brownfield` 同款能力序（decoupling → fit-check → view → 条件 read model）；设计模式支线与 greenfield §2.3 相同——`design-pattern-opportunity-scan` 扫 `<slice>/08-spec.md` 与既有代码，`concerns` 非空才进入 fit/蓝图，蓝图由 s10-s13 对应层消费。

## 3. 门禁（读产物文件核对）

| 门禁 | 位置 | 放行条件 |
| :-- | :-- | :-- |
| G0 现状 | `01-survey.md` 后 | 现状模型可解释现有关键行为；坏味道与行为黑盒已列清 |
| G1 规划 | `03-plan.md` 后 | 切片顺序、回滚策略、特征化测试范围获确认；满足"旧系统始终可运行" |
| G2 切片安全 | 每片落地前（`<slice>/00-characterization.md`）| 特征化测试已覆盖该片现有行为（无裸切）|
| G3 切片验收 | 每片 `<slice>/15-acceptance.md` 后 | 通过契约/不变量/编排/幂等测试；行为与旧实现等价；可切流量且可回滚 |

### 局部模型评估：如何消费 `ddd-model-review`

每个切片的 `<slice>/03-review.md` 只作为客观评估输入：五维评分、问题清单、发现清单与结论。本 workflow 负责把发现映射到切片是否继续、是否停下确认、是否重跑上游能力。不得要求 `ddd-model-review` 决定回溯目标。

### 接口骨架落地：如何消费 `ddd-port-scaffold`

每个切片的 `<slice>/09-scaffold.md` 只提供目标语言分层骨架与契约追踪注释。本 workflow 负责判定骨架是否满足落地门禁：端口契约可表达、依赖只向内、应用层只依赖端口抽象、骨架无业务实现、接口/方法保留不变量与用例编号。

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
