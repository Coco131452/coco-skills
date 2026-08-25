---
name: coco-docs-init
description: 为个人项目创建或从现有代码回补精简、可追溯的工程文档体系；适用于新项目初始化或已有项目缺少准确文档的情况。
---

# Coco 文档初始化

仅创建项目真正需要的文档。先判断是新项目还是已有代码回补；在理解项目前不要生成充满假设的文档。

## 新项目

确认目标用户、核心价值、主要流程、范围、技术约束、运行环境和成功标准。根据实际需要创建：

```text
docs/
  README.md
  specs/PRD.md
  specs/SAD.md
  specs/CODEBASE-ANALYSIS.md
  guides/AI-DEVELOPMENT-GUIDE.md
  guides/RUNBOOK.md
  modules/
  plans/
```

## 已有项目

先使用 `coco-codebase-index` 建立代码证据，再检查 README、配置、入口、路由、数据模型、测试和部署文件。文档必须区分：代码证实、用户确认、合理推断。推断必须写出依据和待确认点。

可按需生成 `docs/specs/CODEBASE-ANALYSIS.md`，记录入口、模块、契约、数据、配置、测试和技术债。不要用“若干模块”之类空泛表述；写出实际路径和接口。

## 规则

- 不覆盖已有有效文档；先比较并合并。
- 文档描述必须与当前代码、配置和测试一致。
- 只创建有内容的文件，不铺设空目录或模板。
- 项目级长期文档放 `docs/specs`、`docs/guides` 或 `docs/modules`；单个需求/缺陷放 `docs/plans/{Work-Item-Key}`。
- `PRD.md`、`SAD.md`、`CODEBASE-ANALYSIS.md`、`AI-DEVELOPMENT-GUIDE.md`、`RUNBOOK.md` 和 `modules/*.md` 是项目长期基线；仅在实际受影响时更新，不要求每个工作项全部修改。
- 发现冲突时列出证据和待确认项，不把推断写成事实。

完成后给出文档索引、来源说明、仍待确认的信息，以及建议的维护触发条件。

## 项目级基础文档

- `docs/specs/PRD.md`：产品目标、角色、核心流程、业务规则和功能范围。
- `docs/specs/SAD.md`：系统边界、架构、模块、数据流、API、数据、安全和部署设计。
- `docs/specs/CODEBASE-ANALYSIS.md`：运行入口、模块地图、接口、数据模型、配置、测试和技术债。
- `docs/guides/AI-DEVELOPMENT-GUIDE.md`：AI 使用边界、需求/缺陷流程、TDD、Git、Review、MCP 和文档规范。
- `docs/guides/RUNBOOK.md`：环境、启动、部署、Migration、监控、故障处理和回滚。
- `docs/modules/*.md`：模块职责、文件位置、公开接口、数据所有权、依赖、配置和测试入口。

初始化时只创建有事实内容的文件；每次交付检查是否受影响，未受影响不修改，但在 `verification.md` 中写明“不适用”及原因。
