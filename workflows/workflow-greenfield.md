# Workflow：Greenfield（0→1 新建）

> 统筹者。本文件是**唯一**掌握顺序、文件交接、门禁与回溯的地方；被调用的 SKILL 都是纯能力，对流程一无所知。由 `/backend-best-practices:ddd-new` 触发。
> 交付链路：战略 DDD → 战术 Domain → **Application 用例编排** → **业务视图/读侧** → 统一契约 → （条件）设计模式 → 分层实现 → 验收。

## 0. 入口路由（原 mode-router 职责，已并入本层）

1. **判定驱动**：无既有实现/愿重写 → greenfield（本流程）；有可运行代码且目标是渐进改造 → 转 `workflow-brownfield`。
2. **采集最小上下文**：一句可被业务方认可的问题陈述、关键参与方、硬约束（合规/时限/团队）。缺阻塞项先问清，不猜。
3. **登记落地语言**：记录 `--lang`（默认延后到 G6 前再定）。
4. **建运行工作区**：创建 `<workdir>/`（默认 `./run/ddd-new/`），写入 `shared/00-routing.md` 与 `_manifest.md`。

## 1. 共享战略段（工件在 `shared/`）

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| 00 | （路由，本层）| 用户诉求 | `shared/00-routing.md` | |
| 01 | ddd-scope | `shared/00-routing.md` | `shared/01-scope.md` | |
| 02 | ddd-discover | `shared/01-scope.md` | `shared/02-discover.md` | |
| 03 | ddd-subdomains | `shared/01-scope.md`,`shared/02-discover.md` | `shared/03-subdomains.md` | |
| 04 | ddd-contexts | `shared/02-discover.md`,`shared/03-subdomains.md` | `shared/04-contexts.md` | |
| 05 | ddd-context-map | `shared/04-contexts.md` | `shared/05-context-map.md` | **G1** |

## 2. 逐上下文循环（每个上下文 `<ctx>` 用独立子工作区 `contexts/<ctx>/`）

`shared/04-contexts.md` 的上下文清单驱动循环，核心域优先。**generic/支撑域上下文**若在 contexts 工件中标注为"买/用现成"（如认证用成熟库、通知用 SaaS），不进战术循环——由本层产出一份 `contexts/<ctx>/00-integration.md`（选型、集成点、该能力对用户诉求的交付归属、ACL 落点），其出入站集成由核心上下文的 c18/c20 消费；该决策记入 `_manifest.md`。

### 2.1 战术建模与 Application 设计

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| c01 | ddd-aggregates | `shared/04-contexts.md`,`shared/05-context-map.md`,`shared/02-discover.md` | `contexts/<ctx>/01-aggregates.md` | |
| c02 | ddd-domain-interactions | `contexts/<ctx>/01-aggregates.md`,`shared/05-context-map.md` | `contexts/<ctx>/02-interactions.md` | |
| c03 | ddd-model-review | `shared/03..05-*.md`,`contexts/<ctx>/01..02-*.md` | `contexts/<ctx>/03-model-review.md` | **G2** |
| c04 | ddd-application-use-cases | `shared/02-discover.md`,`contexts/<ctx>/01..02-*.md` | `contexts/<ctx>/04-use-cases.md` | |
| c05 | ddd-application-orchestration | `contexts/<ctx>/04-use-cases.md`,`contexts/<ctx>/01-aggregates.md` | `contexts/<ctx>/05-orchestration.md` | |
| c06 | ddd-process-manager-design | `contexts/<ctx>/05-orchestration.md`（长流程候选）,`contexts/<ctx>/02-interactions.md` | `contexts/<ctx>/06-process-managers.md` | 条件执行（有长流程候选）|
| c07 | ddd-application-review | `contexts/<ctx>/04,05,06?-*.md` | `contexts/<ctx>/07-application-review.md` | **G3** |

### 2.2 业务视图与读侧（视图先行，逐视图定读侧方案）

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| c08 | cqrs-aggregation-view-design | `shared/01-scope.md`（视图需求种子）,`shared/02-discover.md`（查询/视图目录）,`contexts/<ctx>/01-aggregates.md` | `contexts/<ctx>/08-views.md` | |
| c09 | cqrs-fit-check | `contexts/<ctx>/08-views.md`,`contexts/<ctx>/01-aggregates.md` | `contexts/<ctx>/09-read-fit.md` | |
| c10 | cqrs-domain-read-decoupling | `contexts/<ctx>/08-views.md`,`contexts/<ctx>/01-aggregates.md` | `contexts/<ctx>/10-domain-read-decoupling.md` | |
| c11 | cqrs-read-model-design | `contexts/<ctx>/08..10-*.md` | `contexts/<ctx>/11-read-models.md` | 条件执行（`views` 中存在 `use`）|
| c12 | cqrs-read-model-sync | `contexts/<ctx>/11-read-models.md`,`contexts/<ctx>/05-orchestration.md`（事件/Outbox 衔接）| `contexts/<ctx>/12-read-model-sync.md` | 条件执行（同上）|
| c13 | cqrs-review | `contexts/<ctx>/08,09,10,11?,12?-*.md` | `contexts/<ctx>/13-read-review.md` | **G4** |

`c09`（`09-read-fit.md`）输出逐视图矩阵：`decision=avoid` 的视图仍须在 `08-views.md` 拥有视图契约与权限，走简单查询方案；仅 `decision=use` 的视图进入 c11/c12。

### 2.3 统一契约与（条件）设计模式支线

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| c14 | ddd-spec-bridge | `contexts/<ctx>/02,04,05,06?,08,11?,12?-*.md` | `contexts/<ctx>/14-spec.md` | |
| p01 | design-pattern-opportunity-scan | `contexts/<ctx>/14-spec.md`（+ 既有代码/骨架，0→1 首轮可缺席，仅基于契约扫描）| `contexts/<ctx>/patterns/01-scan.md` | |
| p02 | design-pattern-fit-check | `patterns/01-scan.md` 中单个 concern | `contexts/<ctx>/patterns/02-fit-<concern>.md` | 条件执行（`concerns` 非空，逐 concern）|
| p03 | design-pattern-implementation | `patterns/02-fit-<concern>.md` | `contexts/<ctx>/patterns/03-blueprint-<concern>.md` | 条件执行（`decision=use`）|
| — | （G5 核对，本层）| `14-spec.md` + `patterns/*` | 更新 `_manifest.md` | **G5** |

`p01` 输出 `concerns` 为空 → 直接过 G5（无模式是正当结果）。`p02` 判 `simplify/avoid` → 该 concern 结案，不产蓝图。`p03` 蓝图不写真实代码——由 2.4 中 `owner_layer` 对应的实现步骤消费。

### 2.4 骨架、分层实现与验收

| 序 | 调用能力 | 输入文件 | 输出文件 | 门禁 |
| :-- | :-- | :-- | :-- | :-- |
| c15 | ddd-port-scaffold | `contexts/<ctx>/14-spec.md` + 语言剖面 | `contexts/<ctx>/15-scaffold.md` | **G6** |
| c16 | ddd-domain-impl | `15-scaffold.md`,`14-spec.md`（+ `patterns/03-*` 中 `owner_layer=domain` 的蓝图）| `contexts/<ctx>/16-domain-impl.md` | |
| c17 | ddd-application-impl | `15-scaffold.md`,`14-spec.md`,`05-orchestration.md`,`08-views.md`（`avoid` 视图的查询契约）（+ `patterns/03-*` 中 `owner_layer=application` 的蓝图）| `contexts/<ctx>/17-application-impl.md` | |
| c18 | ddd-outbound-adapter-impl | `15-scaffold.md`,`14-spec.md`（+ `patterns/03-*` 中 `owner_layer=adapter` 的蓝图）| `contexts/<ctx>/18-outbound-impl.md` | |
| c19 | cqrs-read-model-impl | `08-views.md`,`09-read-fit.md`,`11?,12?-*.md`,`15-scaffold.md`（+ `patterns/03-*` 中 `owner_layer=read` 的蓝图）| `contexts/<ctx>/19-read-impl.md` | 条件执行（存在 `use` 视图）|
| c20 | ddd-inbound-adapter-impl | `15-scaffold.md`,`04-use-cases.md` | `contexts/<ctx>/20-inbound-impl.md` | |
| p04 | design-pattern-review | `patterns/03-*` + 对应层实现工件 | `contexts/<ctx>/patterns/04-review.md` | 条件执行（有蓝图）|
| c21 | ddd-acceptance | `14-spec.md`,`16,17,18,19?,20-*.md` | `contexts/<ctx>/21-acceptance.md` | **G7** 之一 |
| c22 | cqrs-read-model-acceptance | `11?,12?-*.md`,`19-read-impl.md` | `contexts/<ctx>/22-read-acceptance.md` | 条件执行（存在 `use` 视图）|
| c23 | ddd-application-review | `contexts/<ctx>/04,05,06?-*.md`,`17-application-impl.md`,`21,22?-*.md`（测试证据来源）| `contexts/<ctx>/23-application-review-impl.md` | **G7** |

验收先行（c21/c22 产出 test_file+test_name+status 证据），实现态应用审查（c23）消费这些证据——测试证据的生产者由此在流程内闭环。

`avoid` 视图的查询交付路径：查询契约（`08-views.md`）由 c17 落成 Query Handler / View DTO（权限下推）、c18 落成 Query Port 的读存储访问；其验收由 c21 的查询类测试义务（无副作用、权限过滤、分页/排序、空结果）承担——`avoid` 不建独立读模型，但查询实现与验收不缺席。

全部上下文完成后，本层汇总 `delivery/acceptance-report.md`（各上下文门禁结果、追踪链核对、遗留项）。

## 3. 门禁（读产物文件核对；这是"两级自检"的第②级）

| 门禁 | 位置 | 放行条件 | 停顿 |
| :-- | :-- | :-- | :-- |
| G1 战略 | `shared/05-context-map.md` 后 | 上下文边界与契约所有权获用户确认；核心域已声明且每个核心上下文有 ACL/隔离 | 停下与用户确认 |
| G2 模型 | `03-model-review.md` 后 | 不变量表达率 ≥ 60%；无阻断级一致性问题；每条目标有建模覆盖；无未决回溯项 | 停下与用户确认 |
| G3 应用设计 | `07-application-review.md` 后 | 无硬门禁命中（清单见 `references/application-review-rubric.md`）；按 rubric 设计态判定 ≥ conditional_pass；每个写命令有唯一 UC；`GOAL→CMD→UC→AGG→INV→EVT→AC` 追踪闭合（环节确实不适用时以显式 `n/a(理由)` 记录视为闭合，如无订阅方的事件）| |
| G4 读侧 | `13-read-review.md` 后 | 每个 VIEW 在 `09-read-fit.md` 的 `views` 矩阵有结论；`avoid` 视图也有视图契约、查询方案与权限；`use` 视图字段有来源、有同步与重建策略；无 critical/high；无默认事件溯源/微服务/双库 | |
| G5 契约与模式 | `14-spec.md` 与 `patterns/*` 后 | 规范自洽（用例/端口/事件/读侧互引都在规范内定义）；每个 `PAT` 有真实 `change_axis` 与更简单替代对比；`concerns` 为空时除 `patterns/01-scan.md`（扫描证据）外无 fit/蓝图/审查工件 | 停下与用户确认 |
| G6 骨架 | `15-scaffold.md` 后 | 端口契约可在目标语言完整表达；依赖只向内——应用层可依赖 Domain 内核，对外部资源只依赖端口抽象；骨架零实现；接口/方法保留不变量与用例编号的契约追踪注释 | 确认落地语言 |
| G7 实现与验收 | `21,22?,23-*.md` 后 | acceptance 全部 INV/AC/测试义务通过并有 test_file+test_name 证据；有读模型时读侧验收通过；实现态 application review 按 rubric 达 **pass**；架构依赖测试通过（领域零基础设施、应用零具体 SDK、入口不直连仓储）| |

### 门禁如何消费审查类工件

审查类能力只输出客观发现与证据供本层判定：`ddd-application-review` 不含任何判定字段；`ddd-model-review` / `cqrs-review` / `design-pattern-review` 的结论字段（如 `overall`）**仅作参考输入**——放行、评分与回溯一律以本 workflow 门禁为准，本层可以且应当覆盖其结论。G3/G7 按 `references/application-review-rubric.md` 计分判定；发现到回溯目标的映射由 §4 决定。

## 4. 回溯矩阵（本层独有；SKILL 不含回溯信息）

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
| 写命令无法映射到唯一 UC | ddd-application-use-cases |
| 编排步骤含业务判断 / 直改实体 | ddd-application-orchestration（改委派）+ ddd-aggregates（规则入聚合）|
| 幂等未覆盖崩溃窗口 | ddd-application-orchestration |
| 存在"已提交但事件丢失"窗口 | ddd-application-orchestration |
| 长流程不可恢复 / 补偿无终点 | ddd-process-manager-design |
| 视图字段无来源 / Domain 被展示字段污染 | cqrs-aggregation-view-design / cqrs-domain-read-decoupling |
| `avoid` 视图直接暴露 Entity | cqrs-domain-read-decoupling |
| 读模型刷新/重建策略缺失 | cqrs-read-model-sync |
| 模式无真实变化轴 / 过度设计 | design-pattern-opportunity-scan（降级 simplify/avoid）|
| 蓝图角色与代码位置对不上 | design-pattern-implementation |
| 端口契约目标语言无法表达 | ddd-spec-bridge |
| 反复并发竞态 | ddd-aggregates |
| 设计态 rubric fail | 按短板维度：D1/D7 → ddd-application-use-cases；D3/D4/D6 → ddd-application-orchestration；D8 → ddd-application-use-cases（补验收准则与负例）|
| 实现态 rubric fail | 对应层实现步骤 + 触发维度的上游设计能力 |

## 5. 编排纪律

- **非一口气跑完**：在 G1/G2/G5 停下与用户确认关键工件。
- **工件即文件**：严格按 §1/§2 的输入/输出文件传递（工件信封：`artifact_schema_version` + Markdown 正文 + `structured_summary`）；SKILL 不自行决定文件名。
- **Application 是必备层**：所有写命令必须经 UC/Handler；Controller 直调仓储或聚合在 G7 架构测试中阻断。
- **业务视图是必经设计，CQRS 是可选实现**：`avoid` 只是不建独立读模型，视图契约、查询方案与权限照常交付。
- **模式是条件支线**：没有变化轴时 `concerns` 为空，只留扫描证据、不产 fit/蓝图/审查工件，这是正确结果而非缺失。
- **语言延后绑定**：落地语言在 G6 前才需确定。
- **回溯是常态**：按 §4 重跑上游并在 `_manifest.md` 记录原因，不算失败。
