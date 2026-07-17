# 能力清单（整理）

把后端最佳实践拆成**纯能力**：只看 输入→输出，剥掉一切上下游/阶段/回溯引用。流程顺序、门禁与回溯由 workflow 负责。

> 命名：保留 `ddd-*` 能力，新增 `cqrs-*` 读模型能力，并新增 `design-pattern-*` 设计模式能力。

## DDD 纯能力表

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 1 | scope | 模糊诉求 → 结构化范围 | 自然语言诉求 | 问题陈述/价值主张/目标·非目标/硬约束/术语种子/**视图需求种子**/风险 |
| 2 | discover | 事件风暴 | 问题陈述 + 术语种子 | 事件流/命令·事件目录/**查询·视图目录**/策略/热点/泳道 |
| 3 | subdomains | 子域三分类 | 事件流 + 泳道 + 价值主张 | 能力清单/子域分类/核心域声明 |
| 4 | contexts | 限界上下文 + 通用语言 | 子域分类 + 热点 + 术语种子 | 上下文目录/各上下文词汇表/边界 ADR |
| 5 | context-map | 上下文映射 | 上下文目录 + 跨界待解 | 关系矩阵/集成模式/契约所有权/一致性语义 |
| 6 | aggregates | 不变量 → 聚合 | 词汇表 + 策略 + 一致性语义 | 不变量表/聚合目录/事务边界/一致性策略 |
| 7 | domain-interactions | 协作接口语义化 | 聚合目录 + 不变量 + 契约所有权 | 事件契约/服务·仓储·工厂接口（中立，领域服务仅纯业务判断）/应用层待办 |
| 8 | model-review | 模型质量评估 | 全部战略+战术工件 | 五维评分/问题清单/**发现**/结论 |
| 9 | spec-bridge | 语言中立完整后端契约规范 | 战术工件 + 应用工件（+可选读侧契约）| Domain 端口/用例契约/出站端口/事件 schema/读侧契约/可靠性语义/不变量命题/验收准则 |
| 10 | port-scaffold | 按语言剖面生成分层项目骨架 | 后端契约规范 + 语言剖面 | 分层骨架/端口与 Input Port 接口/值对象骨架/测试占位/待实现清单 |
| 11 | ~~adapter-impl~~ | **已移除（0.3.0）**——由 52-55 分层实现能力替代；编号空缺保留至统一重排 | — | — |
| 12 | acceptance | 面向接口验收 | 不变量命题 + 验收准则 + 实现 | 测试集/验收报告 |
| 13 | code-survey | 逆向重建现状模型 | 代码库 + 改造目标 | 现状模型/隐含上下文/规则打捞/坏味道/行为黑盒 |
| 14 | seam-finder | 接缝与防腐层识别 | 现状模型 + 坏味道 | 接缝清单/ACL 落点/切割风险/特征化测试需求 |
| 15 | strangler-plan | 绞杀者迁移计划 | 接缝 + ACL + 风险 | 切片清单/批次顺序/切换·回滚策略/DoD/退役计划 |

## CQRS Read Model 纯能力表

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 16 | cqrs-fit-check | **逐视图**判断是否需要 CQRS 式读模型分离 | 目标视图清单 + 业务目标 + 当前模型 + 约束 | 逐视图矩阵（decision/驱动/最小方案）+ 总体决策、风险、不推荐模式 |
| 17 | cqrs-domain-read-decoupling | 划清 Domain 与展示查询职责 | 实体/聚合 + 用例 + UI/API + 痛点 | 领域职责、读侧职责、污染迹象、解耦动作、字段真源 |
| 18 | cqrs-aggregation-view-design | 设计业务聚合视图 | 视图目标 + 字段 + 筛选排序聚合 + 来源 + 新鲜度 | 视图契约、字段来源、派生规则、权限、性能需求 |
| 19 | cqrs-read-model-design | 把视图转成具体读模型 | 聚合视图 + 真源 + 查询模式 + 性能目标 | 模型类型、字段映射、索引、查询契约、所有权 |
| 20 | cqrs-read-model-sync | 选择读模型刷新策略 | 读模型 + 真源 + 新鲜度 + 读写频率 + 基础设施 | 同步策略、刷新时机、失败处理、重建策略、风险和回退 |
| 21 | cqrs-review | 审查读模型方案 | 适配判断 + 视图 + 读模型 + 同步策略 + API/迁移设计 | pass/needs_changes/fail、分级发现、最小修正、下一步 |

## Design Pattern 纯能力表

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 22 | design-pattern-fit-check | 判断是否需要模式并选择最小可行模式 | 设计问题 + 代码上下文 + 变化轴 + 约束 + 目标语言 | Markdown 适配说明 + structured_summary（decision/change_axis/primary_pattern/simpler_alternative 等，串接必备）|
| 23 | design-pattern-abstract-factory | 抽象工厂最佳实践 | 产品族变化 + 配套对象约束 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 24 | design-pattern-builder | 建造者最佳实践 | 复杂构造 + 参数/校验/默认值 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 25 | design-pattern-factory-method | 工厂方法最佳实践 | 创建扩展点 + 产品抽象 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 26 | design-pattern-prototype | 原型最佳实践 | 克隆模板 + 拷贝边界 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 27 | design-pattern-singleton | 单例最佳实践 | 进程级唯一资源 + 生命周期约束 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 28 | design-pattern-adapter | 适配器最佳实践 | 不兼容接口 + 外部/遗留系统 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 29 | design-pattern-bridge | 桥接最佳实践 | 双变化维度 + 抽象/实现分离 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 30 | design-pattern-composite | 组合最佳实践 | 树结构 + 个体/组合统一处理 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 31 | design-pattern-decorator | 装饰器最佳实践 | 可组合增强 + 稳定接口 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 32 | design-pattern-facade | 外观最佳实践 | 复杂子系统 + 简化入口 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 33 | design-pattern-flyweight | 享元最佳实践 | 大量重复对象 + 不可变共享 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 34 | design-pattern-proxy | 代理最佳实践 | 访问控制/远程/缓存/懒加载 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 35 | design-pattern-chain-of-responsibility | 责任链最佳实践 | 处理链 + 顺序/短路语义 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 36 | design-pattern-command | 命令最佳实践 | 可排队/审计/撤销请求 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 37 | design-pattern-interpreter | 解释器最佳实践 | 小语言/DSL + 表达式树 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 38 | design-pattern-iterator | 迭代器最佳实践 | 自定义集合/分页/流式访问 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 39 | design-pattern-mediator | 中介者最佳实践 | 多对象复杂协作 + 解耦参与者 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 40 | design-pattern-memento | 备忘录最佳实践 | 快照/撤销/恢复 + 状态封装 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 41 | design-pattern-observer | 观察者最佳实践 | 一对多通知 + 订阅者隔离 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 42 | design-pattern-state | 状态模式最佳实践 | 生命周期状态 + 状态相关行为 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 43 | design-pattern-strategy | 策略最佳实践 | 可替换算法 + 稳定上下文 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 44 | design-pattern-template-method | 模板方法最佳实践 | 固定流程骨架 + 可变步骤 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 45 | design-pattern-visitor | 访问者最佳实践 | 稳定对象结构 + 新增操作 + 目标语言 | Markdown 设计说明、语言差异附件、案例附件、可选 structured_summary |
| 46 | design-pattern-implementation | 将模式转成实现蓝图（语言无关结构 + 目标语言惯用示意，真实代码归所属层实现能力）| 模式决策 + 具体模式指南 + 业务角色 + 目标语言 + 约束 + 现有接口 | Markdown 蓝图 + structured_summary（owner_layer/role_mapping/target_code_paths/test_obligations 等）|
| 47 | design-pattern-review | 审查模式是否必要、角色是否清楚、实现是否惯用 | 模式方案/代码 + 目标语言 + 设计目标 + 测试 | Markdown 审查报告、分级发现、更简单替代方案、可选 structured_summary |

## Application 纯能力表（新增）

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 48 | ddd-application-use-cases | 参与者/命令/策略 → 应用用例目录 | 发现工件 + 战术工件 | 用例目录（Input Port/Command·Result/授权分层/领域调用/错误语义）/追踪表 |
| 49 | ddd-application-orchestration | 用例执行编排设计 | 用例目录 + 一致性策略 + 可靠性要求 | 编排表（步骤/事务/幂等/事件投递/重试/可观测）/长流程候选 |
| 50 | ddd-process-manager-design | 长流程 none/choreography/PM 决策与设计（条件）| 长流程候选 + 事件契约 | 流程决策表/PM 设计（状态/迁移/超时/补偿/恢复）|
| 51 | ddd-application-review | 应用层设计/实现客观审查 | 用例目录 + 编排（实现态另需代码与测试证据）| 检查项证据表/分级发现/硬约束触发/结论（不打分）|

## 分层实现纯能力表（替代已移除的 adapter-impl）

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 52 | ddd-domain-impl | 实现领域层 | 骨架 + 契约语义 + 不变量 + 剖面 | 值对象/聚合/领域服务/领域事件实现（零基础设施）|
| 53 | ddd-application-impl | 实现应用层 | 用例契约 + 编排 + 骨架 + 剖面 | Command/Query Handler（固定形状）/事件处理器/错误映射 |
| 54 | ddd-inbound-adapter-impl | 实现入站适配器 | 入口清单 + 用例契约 + 剖面 | Controller/Consumer/Job/CLI → Input Port 映射 + 认证 + 协议错误映射 |
| 55 | ddd-outbound-adapter-impl | 实现出站适配器与装配 | 出站端口契约 + 事务/投递要求 + 剖面 | 仓储/UoW/Outbox·Inbox/网关 ACL/Read Store/Composition Root |

## 读侧交付纯能力表（新增）

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 56 | cqrs-read-model-impl | 读侧实现 | 视图契约 + 读模型设计 + 同步策略 | Query Handler/View DTO/Reader/Projection/读存储/Checkpoint/迁移重建（权限下推）|
| 57 | cqrs-read-model-acceptance | 读侧验收 | 读模型设计 + 同步策略 + 实现 | 10 类验收测试集 + 报告（每项 pass/fail + 测试名证据）|

## 模式机会扫描（新增）

| # | 能力 | 做什么 | 输入（数据形状）| 返回（数据形状）|
| :-- | :-- | :-- | :-- | :-- |
| 58 | design-pattern-opportunity-scan | 扫描真实变化轴，产出模式关注点清单（空清单是正当结果）| 分层契约 + 代码/骨架 + 已知变体与约束 | Markdown 扫描说明 + structured_summary（concerns：owner_layer/change_axis/evidence/simpler_alternatives 等）|

## 两个耦合点的处置

- **`ddd-mode-router`（原第 0 个）不再是 skill。** 它的职责是"判定驱动、分流入口"——本质是编排/分流，属 workflow/command 层。→ **从 skills 移除**，逻辑下沉到流程入口。
- **`model-review` 去掉"回退到某 skill"。** 纯能力只输出评分 + 客观**发现清单**（哪条不变量没被强制、哪个目标没覆盖……）；把发现映射成"回退到哪一步"是 **workflow** 的回溯规则，不写进 skill。

## 影响

- 当前能力总数 **57**（DDD 14 + CQRS 6 + Design Pattern 26 + Application 4 + 分层实现 4 + 读侧交付 2 + 模式扫描 1；adapter-impl 已于 0.3.0 移除）。
- skills 从 16 → **15**（移除 mode-router）。
- 每个 skill 正文从"七段（含使用时机/回溯触发）" → "四段必需可扩充（做什么/参数/怎么做/返回）"；示例等重内容移到同目录附加文件（`examples.md` 等），按需加载。
- 阶段顺序、门禁阈值（如模型评估的量化标准）、回溯矩阵——**全部迁到 workflow**。
