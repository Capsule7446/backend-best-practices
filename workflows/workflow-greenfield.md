# Workflow：Greenfield（0→1 新建）

> 统筹者。本文件是**唯一**掌握顺序、文件交接、门禁与回溯的地方；被调用的 SKILL 都是纯能力，对流程一无所知。由 `/backend-best-practices:ddd-new` 触发。

## 0. 入口路由（原 mode-router 职责，已并入本层）

workflow 启动时先自行完成分流，不再有独立的 router skill：

1. **判定驱动**：无既有实现/愿重写 → greenfield（本流程）；有可运行代码且目标是渐进改造 → 转 `workflow-brownfield`。
2. **采集最小上下文**：一句可被业务方认可的问题陈述、关键参与方、硬约束（合规/时限/团队）。缺阻塞项先问清，不猜。
3. **登记落地语言**：记录 `--lang`（默认延后到 G3 前再定）。
4. **建运行工作区**：创建 `<workdir>/`（默认 `./run/`），写入 `00-routing.md` 与 `_manifest.md`。

## 1. 工作区与文件交接

每个 SKILL 只被告知「读哪些输入文件、写哪个输出文件」；文件名与编号由本 workflow 统一分配。

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 00 | （路由，本层）| 用户诉求 | `00-routing.md` | |
| 01 | ddd-scope | `00-routing.md` | `01-scope.md` | |
| 02 | ddd-discover | `01-scope.md` | `02-discover.md` | |
| 03 | ddd-subdomains | `01-scope.md`,`02-discover.md` | `03-subdomains.md` | |
| 04 | ddd-contexts | `02-discover.md`,`03-subdomains.md` | `04-contexts.md` | |
| 05 | ddd-context-map | `04-contexts.md` | `05-context-map.md` | **G1** |
| 06 | ddd-aggregates | `04-contexts.md`,`05-context-map.md`,`02-discover.md` | `06-aggregates.md` | |
| 07 | ddd-domain-interactions | `06-aggregates.md`,`05-context-map.md` | `07-interactions.md` | |
| 08 | ddd-model-review | `03..07-*.md`（全战略+战术）| `08-review.md` | **G2** |
| 09 | ddd-spec-bridge | `06-aggregates.md`,`07-interactions.md` | `09-spec.md` | |
| 10 | ddd-port-scaffold | `09-spec.md` + 语言剖面 | `10-ports.md` | **G3** |
| 11 | ddd-adapter-impl | `10-ports.md`,`09-spec.md` | `11-impl.md` | |
| 12 | ddd-acceptance | `09-spec.md`,`11-impl.md` | `12-acceptance.md` | |

workflow 每步后更新 `_manifest.md`：阶段状态、门禁结果、回溯记录。

## 2. 门禁（读产物文件核对；这是"两级自检"的第②级）

SKILL 只保证自己产物**格式**合格；能否放行由本层判定：

| 门禁 | 位置 | 放行条件（读对应文件核对）| 停顿 |
| :-- | :-- | :-- | :-- |
| G1 战略 | `05-context-map.md` 后 | 上下文边界与契约所有权获用户确认；核心域已声明且每个核心上下文有 ACL/隔离 | 停下与用户确认 |
| G2 模型 | `08-review.md` 后 | 不变量表达率 ≥ 60%；无阻断级一致性问题；每条目标有建模覆盖；无未决回溯项 | 停下与用户确认 |
| G3 落地 | `10-ports.md` 后 | 端口契约可在目标语言完整表达；依赖只向内；骨架零实现 | 确认落地语言 |

## 3. 回溯矩阵（本层独有；SKILL 不含回溯信息）

门禁不过时，本层按下表**重跑对应上游 SKILL**（把修正说明作为额外输入文件传入）。`ddd-model-review` 只提供客观发现，映射到哪一步由本表决定：

| 触发条件（来自产物/门禁）| 重跑 |
| :-- | :-- |
| 价值主张不清 / 目标自相矛盾 | ddd-scope |
| 事件流与目标矛盾 / 热点纠缠 | ddd-scope |
| 能力无法归类（缺事件）| ddd-discover |
| 找不到/超过 3 个核心域 | ddd-scope |
| 核心能力被劈到两上下文 | ddd-subdomains |
| 同名异义未被边界切开 | ddd-discover |
| 关系无论如何都强耦合 | ddd-contexts |
| 不变量需跨上下文强制 | ddd-contexts / ddd-context-map |
| 列不变量时缺触发事件 | ddd-discover |
| 事件需携带他聚合私有数据 | ddd-aggregates |
| 不变量表达率 < 60% / 数据袋聚合 | ddd-aggregates |
| 某目标无建模覆盖 | ddd-discover / ddd-scope |
| 契约语义无法中立化 | ddd-domain-interactions |
| 不变量无法写成可观测断言 | ddd-aggregates |
| 端口契约目标语言无法表达 | ddd-spec-bridge |
| 反复并发竞态 | ddd-aggregates |

## 4. 编排纪律

- **非一口气跑完**：在 G1/G2 停下与用户确认关键工件。
- **工件即文件**：严格按 §1 的输入/输出文件传递，不在阶段间丢信息；SKILL 不自行决定文件名。
- **语言延后绑定**：落地语言在 G3 前才需确定。
- **回溯是常态**：按 §3 重跑上游并在 `_manifest.md` 记录原因，不算失败。
