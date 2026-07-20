# DDD 后端交付系统改造蓝图（修订版）

> 本文件是本仓库从"若干独立最佳实践 Skill"升级为"完整 DDD 后端交付系统"的实施真源。
> 源于外部重构建议文档，经与仓库现状逐条核对后修订；已落地部分以仓库文件为准，本文只保留追踪与未尽事项。

## 1. 目标链路

```text
业务范围 → 战略 DDD → 战术 Domain → Application 用例编排 → 业务视图/查询侧
→ 统一契约 → 条件式设计模式强化（蓝图）→ 项目骨架 → 分层实现（消费蓝图）→ 业务与架构验收
```

三个原则：

- **Application 是必备层**：所有写命令经 Use Case/Handler，Controller 不直连 Repository/Aggregate。
- **业务视图是必经设计，CQRS 是可选实现**：`avoid` 也要产出 View DTO、查询方案与权限设计。
- **模式只在真实变化轴存在时启用**：空扫描清单是正当结果。

## 2. 对原建议文档的事实修正（核对结论）

| 原表述 | 核对结论 |
| :-- | :-- |
| "嵌套 workflow 导致多 manifest、回溯所有权不清" | 原仓库无嵌套；作为**预防性规则**保留（已固化进 ARCHITECTURE.md workflow 互斥规则）|
| "先 fit-check 再设计 View，判断依据不足" | 入口已采集粗粒度诉求；真正问题是 fit-check 是全局结论 → 已改逐视图矩阵 + 视图先行 |
| "design-pattern-implementation 直接产代码" | 已是 markdown-first；本次仅明确蓝图定位 + `owner_layer` 归属 |
| "spec-bridge 不含 Event" | 原本已含 Domain Event schema；扩容的是用例契约、集成事件、幂等、读侧、可靠性语义 |

## 3. 已落地（0.2.0，本分支）

### P0 契约修复
- `design-pattern-fit-check` 补 `decision/change_axis/primary_pattern/simpler_alternative`，与 `workflow-design-pattern` 门禁对齐。
- CQRS `avoid` 不再中断：轻量读侧路径（视图契约/查询方案/权限照常交付）。
- `workflow-read-model-review` 补析后强制复审（G1 + 循环上限）。
- 工件信封（`artifact_schema_version: 2` + Markdown 正文 + `structured_summary`）与 workflow 互斥规则、统一 ID 体系写入 `docs/ARCHITECTURE.md`。
- 各 workflow 默认工作区改为 `./run/<flow>/`。

### P1 Application 层
- 新增设计态能力：`ddd-application-use-cases` / `ddd-application-orchestration` / `ddd-process-manager-design`（条件）/ `ddd-application-review`（只产证据，不打分）。
- 评分规则（8 维权重、13 条硬门禁、pass/conditional/fail）归 workflow 门禁，见 `references/application-review-rubric.md`。
- `ddd-adapter-impl` 拆为 `ddd-domain-impl` / `ddd-application-impl` / `ddd-inbound-adapter-impl` / `ddd-outbound-adapter-impl`；原能力标废弃（0.3.0 移除）。
- `ddd-domain-interactions` 修界：领域服务只留跨聚合纯业务判断；带 I/O 的编排登记为应用层待办。
- `ddd-spec-bridge` 扩为完整后端契约；`ddd-port-scaffold` 扩为分层项目骨架；`ddd-acceptance` 补编排/事务/幂等验收。
- 语言剖面拆为 `references/language-profiles/<lang>.md`（八层构造映射，按需加载单文件）。
- `workflow-greenfield` 重构：`shared/` 战略段 + `contexts/<ctx>/` 逐上下文循环 + G1-G7 门禁；`workflow-brownfield` 切片循环接入同批能力。

### P2 读侧交付
- `ddd-scope` 增业务视图需求种子；`ddd-discover` 增查询/视图发现链。
- `cqrs-fit-check` 改逐视图矩阵（总体 decision 由视图结论聚合）。
- 新增 `cqrs-read-model-impl`（权限下推、投影幂等、checkpoint）与 `cqrs-read-model-acceptance`（10 类验收 + 测试名证据）。
- read-model 两条 workflow 改"视图先行 + 逐视图路由 + 可选实现/验收"；brownfield 版内建 Backfill → Shadow Read → Parity Diff → Cutover → Rollback 迁移步骤。
- `workflow-system-model-view-read` 同步视图先行与逐视图评估语义。

### P3 设计模式条件支线
- 新增 `design-pattern-opportunity-scan`（变化轴扫描，空清单正当）。
- `design-pattern-implementation` 定位为蓝图（`owner_layer/role_mapping/target_code_paths/test_obligations`），真实代码由所属层实现能力落地。
- greenfield/brownfield 在契约稳定后接条件模式支线：scan → fit → 蓝图 → 层内实现 → pattern review；`workflow-design-pattern` 保留独立入口。

### 校验基建
- `scripts/validate_skills.py` / `validate_plugin.py` + GitHub Actions `validate.yml`。

## 4. 统一门禁总览（greenfield 主流程）

| 门禁 | 放行要点 | 强确认 |
| :-- | :-- | :-- |
| G1 战略 | 上下文边界/契约所有权/核心域 ACL | 用户确认 |
| G2 模型 | 不变量表达率 ≥60%、无阻断一致性问题 | 用户确认 |
| G3 应用设计 | 无硬门禁；rubric ≥ conditional_pass；写命令↔UC 唯一；追踪闭合 | |
| G4 读侧 | 逐视图结论齐全；avoid 也有查询方案与权限；use 有来源与同步 | |
| G5 契约与模式 | 规范自洽；PAT 有真实变化轴；空扫描零模式工件 | 用户确认 |
| G6 骨架 | 契约可表达、依赖只向内、骨架零实现 | 确认语言 |
| G7 实现与验收 | 实现态 rubric pass；架构测试三禁令；INV/AC/义务全通过带测试名证据 | |

## 5. 未尽事项（后续版本）

| 事项 | 版本 | 说明 |
| :-- | :-- | :-- |
| ~~P4 前向验证任务集~~ | ~~0.2.x~~ | **已完成**：`examples/validation-tasks/` 六任务 + 判据；任务 01 已 dogfooding 首跑（判据 10/10 pass，见 `RESULTS-01.md`）；任务 02-06 待执行 |
| ~~validate-traceability 脚本~~ | ~~0.2.x~~ | **已完成**：`scripts/validate_traceability.py`（信封/引用即定义/UC↔INV·AC/VIEW↔fit），已在真实 run 工件上验证 |
| **小需求轻量模式** | 0.3.0 | 任务 01 试跑实测：25 个流程工件对单聚合 CRUD 过重，可合并到 ~9 个（方案见 RESULTS-01 引用的摩擦报告 §4）；触发条件：核心上下文 ≤1、聚合 ≤2、无长流程、fit 全 avoid |
| 实现步骤定位澄清 | 0.3.0 | c16-c20 产"实现说明工件"还是真实工程？G7 的 test status 证据依赖真实工程——需在 ARCHITECTURE 明确两种运行模式（设计交付 / 代码交付）及各自的 G7 判据 |
| 审查 skill 去判定化 | 0.3.0 | `cqrs-review`/`ddd-model-review` 的 `overall`/结论字段与"审查只出证据"纪律不符（当前 workflow 侧已声明结论仅作参考）；统一到 ddd-application-review 的纯证据形态 |
| design-pattern 家族 frontmatter 统一 | 0.3.0 | 26 个 design-pattern-* skill 补 risk/category/inputs/outputs/tags（opportunity-scan 已补）|
| spec-bridge 紧凑化 | 0.3.0 | 小系统下 spec 约 80% 是上游复述；改为"引用 ID + 只写增量语义"的组装形态 |
| ~~ddd-adapter-impl 移除~~ | ~~0.3.0~~ | **已完成**（提前执行）：技能目录删除，CAPABILITIES 编号 11 标空缺，无 workflow/command 引用|
| CAPABILITIES 编号重排 | 0.3.0 | 当前新增能力追加编号（48-58），下个破坏性版本统一重排 |
| Keystone marketplace 发布 | 每版本 | pack.ps1 打包 → dist zip → marketplace by-reference 更新 |

## 6. 架构对齐守则（新增能力时必须遵守）

1. 门禁阈值、评分、回溯映射只写在 workflow / references（rubric），SKILL 只产证据。
2. SKILL 输入一律数据形状（"一份含 {…} 的工件"），禁止"来自 X skill"。
3. SKILL.md 只留四段 + 指路，大 YAML 模板与走查进 `examples.md`/`reference.md`。
4. workflow 依赖的每个 `structured_summary` 字段必须出现在对应 SKILL 的"返回什么"里。
5. 新增 workflow 必须声明专属默认工作区 `./run/<flow>/` 并独占 `_manifest.md`。
