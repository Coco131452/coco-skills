---
name: coco-docs-init
description: 按团队固定目录为项目创建或从现有代码回补可追溯的工程文档体系。
---

# Coco 团队文档初始化

仅创建项目真正需要的文档。先判断是新项目还是已有代码回补；在理解项目前不要生成充满假设的文档。目录和文件命名必须遵循 [团队文档目录契约](references/docs-structure-contract.md)。

## 模式判断

- 已有实质代码，或用户要求根据代码回补：模式 B。
- 尚无实质代码，以需求建立项目：模式 A。
- 生成前说明模式和文件范围；缺失信息会改变产物内容时再请求确认。

## 新项目

确认目标用户、核心价值、主要流程、范围、技术约束、运行环境和成功标准。使用团队固定结构：

```text
docs/
  README.md
  specs/PRD.md
  specs/SAD.md
  guides/AI-DEVELOPMENT-GUIDE.md
  guides/RUNBOOK.md（按需）
  modules/{module-name}.md（按需）
  database/SCHEMA.md（按需）
  database/MIGRATIONS.md（按需）
  api/api-spec.md（按需）
  plans/
```

## 已有项目

先检查 README、配置、入口、路由、数据模型、测试和部署文件，建立代码证据。文档必须区分：代码证实、用户确认、合理推断。推断必须写出依据和待确认点。

模式 B 默认生成 `docs/specs/CODEBASE-ANALYSIS.md`，记录入口、模块、契约、数据、配置、测试和技术债。存在数据库、迁移或外部接口时，同步生成 `docs/database/*` 和 `docs/api/api-spec.md`。不要用“若干模块”之类空泛表述；写出实际路径和接口。

## 规则

- 不覆盖已有有效文档；先比较并合并。
- 文档描述必须与当前代码、配置和测试一致。
- 只创建有内容的文件，不铺设空目录或模板。
- 项目级长期文档固定放 `docs/specs`、`docs/guides`、`docs/modules`、`docs/database` 和 `docs/api`；单个需求/缺陷放 `docs/plans/{Work-Item-Key}`。
- `PRD.md`、`SAD.md`、`CODEBASE-ANALYSIS.md`、`AI-DEVELOPMENT-GUIDE.md`、`RUNBOOK.md`、`modules/*.md`、`database/*.md` 和 `api/api-spec.md` 是项目长期基线；仅在实际受影响时更新。
- 发现冲突时列出证据和待确认项，不把推断写成事实。

完成后给出文档索引、来源说明、仍待确认的信息，以及建议的维护触发条件。

## 项目级基础文档

- `docs/specs/PRD.md`：产品目标、角色、核心流程、业务规则和功能范围。
- `docs/specs/SAD.md`：系统边界、架构、模块、数据流、API、数据、安全和部署设计。
- `docs/specs/CODEBASE-ANALYSIS.md`：运行入口、模块地图、接口、数据模型、配置、测试和技术债。
- `docs/guides/AI-DEVELOPMENT-GUIDE.md`：AI 使用边界、需求/缺陷流程、TDD、Git、Review、MCP 和文档规范。
- `docs/guides/RUNBOOK.md`：环境、启动、部署、Migration、监控、故障处理和回滚。
- `docs/modules/*.md`：模块职责、文件位置、公开接口、数据所有权、依赖、配置和测试入口。
- `docs/database/SCHEMA.md`：实体、字段、关系、约束、索引和数据生命周期。
- `docs/database/MIGRATIONS.md`：迁移历史、执行顺序、兼容、回滚和数据处理。
- `docs/api/api-spec.md`：API/CLI/RPC/Webhook/任务契约、鉴权、输入输出和错误模型。
- `docs/plans/{Work-Item-Key}/`：单个需求、缺陷、计划、设计和验证产物。

初始化时只创建有事实内容的文件；每次交付检查是否受影响，未受影响不修改，但在 `verification.md` 中写明“不适用”及原因。

## 输出规范

只输出完成任务所需的核心内容；删除客套话、长篇铺垫、重复信息和无关说明。代码、文档和注释保持最小必要范围，不添加冗余注释。需要报告时优先给出结论、变更、验证结果和阻塞项。
