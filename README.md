# Coco Skills

一套供个人使用的 Codex 软件开发技能，参考 CMMI、规格驱动开发、证据驱动验证和 AI 原生 SDLC 方法设计。

这些技能统一使用 `coco-` 前缀，不依赖 `aile-*` 或 `superpowers`，覆盖需求、缺陷、设计、计划、开发、测试、审查、验证和交付。

## 项目特点

- 需求和缺陷分流：缺陷先分析复现证据、根因、改动范围和测试影响。
- 分级变更控制：开发中的人工测试反馈按 L0-L4 处理，小细节只更新最小必要文件。
- 证据驱动验证：Build 成功不能替代 API、数据库、浏览器和真实运行时验证。
- 增量代码索引：快速整理入口、符号、依赖、功能影响和测试范围。
- 项目可配置：不硬编码固定工期或覆盖率，优先服从项目规则。

## MCP 集成规则

- 遇到 Jira 单号、Jira 链接或明确来自 Jira 的需求/缺陷时，优先使用 Jira MCP 读取 Issue，并按需读取评论、附件和关联事项。
- 涉及 Server、后端 API、接口参数、请求响应、鉴权或错误码时，优先使用 Apifox MCP 刷新并读取最新 OpenAPI 契约。
- Jira、Apifox、代码和实际运行结果不一致时，必须明确列出差异，不能静默选择其中一份作为正确答案。
- Jira 评论、状态、字段、附件，以及 Apifox 接口的写操作都需要用户明确授权；默认仅执行读取和分析。

## 技能目录

| Skill | 用途 |
| --- | --- |
| `coco-workflow-routing` | 判断需求、缺陷、技术债和开发中变更的处理路径 |
| `coco-docs-init` | 初始化或回补项目工程文档 |
| `coco-codebase-index` | 建立、查询、刷新和验证代码库索引 |
| `coco-requirement-analysis` | 需求、范围、用户故事、验收标准和风险分析 |
| `coco-defect-analysis` | 缺陷复现、根因、影响范围和回归测试分析 |
| `coco-product-design` | UI、交互、页面状态和可访问性设计 |
| `coco-technical-design` | 架构、API、数据库、权限、安全和可观测性设计 |
| `coco-writing-plans` | 将分析和设计拆成可执行计划 |
| `coco-change-control` | 管理人工测试反馈和开发方向调整 |
| `coco-git-worktrees` | 创建和验证隔离 Git 工作区 |
| `coco-executing-plans` | 按计划和垂直切片执行开发 |
| `coco-tdd` | 执行 RED -> GREEN -> REFACTOR |
| `coco-subagent-dev` | 用户明确要求时编排并行子代理开发 |
| `coco-debugging` | 证据驱动的复现、假设验证和根因定位 |
| `coco-code-review` | 功能、架构、安全、性能和测试审查 |
| `coco-verification` | 收集测试和 Runtime 验证凭据 |
| `coco-delivery-report` | 生成验收、交付摘要和残余风险记录 |

## 安装

安装前可以先查看仓库内可用的 skill：

```powershell
npx skills add Coco131452/coco-skills --list
```

### 安装全部 skill

```powershell
npx skills add Coco131452/coco-skills --all -g
```

`-g` 表示安装到用户级；`--all` 表示安装仓库中的全部 skill，并跳过选择步骤。

### 安装指定 skill

```powershell
npx skills add Coco131452/coco-skills `
  --skill coco-workflow-routing coco-codebase-index coco-requirement-analysis `
  -g -y
```

也可以使用完整 GitHub 地址：

```powershell
npx skills add https://github.com/Coco131452/coco-skills.git `
  --skill coco-defect-analysis `
  -g -y
```

### 查看已安装 skill

```powershell
npx skills list -g
```

如果不使用 `-g`，Skills CLI 默认根据当前位置安装为项目级 skill。

## 更新

Skills CLI 当前没有单独的检查命令；使用 `update` 会检查并更新已安装 skill。

更新全部全局 skill：

```powershell
npx skills update -g -y
```

更新单个 skill：

```powershell
npx skills update coco-codebase-index -g -y
```

删除指定 skill：

```powershell
npx skills remove coco-codebase-index -g -y
```

更新完成后重新打开 Codex 会话，以加载最新技能描述。

### 手动安装备用方式

仅当 Skills CLI 无法使用时，才手动将完整的 `coco-*` 目录复制到：

```text
%USERPROFILE%\.codex\skills\
```

不要只复制 `SKILL.md`，否则可能遗漏 `agents/`、`references/` 或 `scripts/`。

## 使用

Codex 可以根据描述自动选择技能，也可以显式调用：

```text
使用 $coco-workflow-routing 判断这个工作项应该走需求还是缺陷流程。
```

需求分析：

```text
使用 $coco-requirement-analysis 分析这个新功能。
```

缺陷分析：

```text
使用 $coco-defect-analysis 分析问题根因、影响范围和回归测试范围。
```

开发执行：

```text
使用 $coco-writing-plans 生成开发计划。
使用 $coco-executing-plans 执行已确认计划。
```

### 需求流程

```text
coco-workflow-routing
 -> coco-codebase-index
 -> coco-requirement-analysis
 -> coco-product-design（涉及 UI 时）
 -> coco-technical-design
 -> coco-writing-plans
 -> coco-tdd / coco-executing-plans
 -> coco-code-review
 -> coco-verification
 -> coco-delivery-report
```

### 缺陷流程

```text
coco-workflow-routing
 -> coco-codebase-index
 -> coco-defect-analysis
 -> coco-debugging
 -> coco-tdd / coco-executing-plans
 -> coco-code-review
 -> coco-verification
 -> coco-delivery-report
```

工作项文档默认放在项目内：

```text
docs/coco/{work-item-id}/
```

`index.md` 记录类型、状态、当前基线和产物；`change-log.md` 记录人工测试反馈和变更决策。

## 代码库索引

`coco-codebase-index` 在目标项目的 `.coco/codebase-index/` 生成本地索引：

```powershell
python scripts/codebase_index.py initialize --root <project-path>
python scripts/codebase_index.py validate --root <project-path>
python scripts/codebase_index.py refresh --root <project-path>
python scripts/codebase_index.py query <term> --root <project-path>
python scripts/codebase_index.py impact src/service.py --root <project-path>
```

索引默认排除 `.env`、密钥、证书、依赖、构建产物和缓存。索引只用于导航和影响分析，修改前仍需打开实际代码确认。

## 安全与维护

- 不要提交 `.env`、API Key、密码、证书、个人 Token 或项目生成的 `.coco/` 索引。
- 修改 skill 后先运行相关脚本测试和结构校验。
- 重大流程调整应同步更新相关 `SKILL.md`、参考文件和 README。
- 提交、推送、创建 PR、部署和外部工单同步都需要明确授权。

## License

当前仓库尚未指定开源许可证。需要公开授权他人使用或修改时，请增加合适的 `LICENSE` 文件。
