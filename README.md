# Coco Skills

一套供个人使用的 Codex 软件开发技能，参考 CMMI、规格驱动开发、证据驱动验证和 AI 原生 SDLC 方法设计。

这些技能统一使用 `coco-` 前缀，不依赖 `aile-*` 或 `superpowers`，覆盖需求、缺陷、设计、计划、开发、测试、审查、验证和交付。

## 项目特点

- 需求和缺陷分流：缺陷先分析复现证据、根因、改动范围和测试影响。
- 分级变更控制：开发中的人工测试反馈按 L0-L4 处理，小细节只更新最小必要文件。
- 证据驱动验证：Build 成功不能替代 API、数据库、浏览器和真实运行时验证。
- 增量代码索引：快速整理入口、符号、依赖、功能影响和测试范围。
- 项目可配置：不硬编码固定工期或覆盖率，优先服从项目规则。

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

### 安装单个 skill

使用 Codex 内置 Skill Installer：

```powershell
$installer = "$HOME\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py"

python $installer `
  --repo Coco131452/coco-skills `
  --path coco-workflow-routing
```

将 `--path` 替换为需要的 skill 目录名。

### 安装全部 skill

```powershell
$repo = "$HOME\Documents\coco-skills"
git clone https://github.com/Coco131452/coco-skills.git $repo

Get-ChildItem $repo -Directory -Filter "coco-*" |
  Copy-Item -Destination "$HOME\.codex\skills" -Recurse -Force
```

也可以手动将目标 `coco-*` 目录复制到：

```text
%USERPROFILE%\.codex\skills\
```

必须复制完整目录，不要只复制 `SKILL.md`，否则可能遗漏 `agents/`、`references/` 或 `scripts/`。

## 更新

如果通过 Git 仓库维护：

```powershell
$repo = "$HOME\Documents\coco-skills"
Set-Location $repo
git pull --ff-only origin main

Get-ChildItem $repo -Directory -Filter "coco-*" |
  Copy-Item -Destination "$HOME\.codex\skills" -Recurse -Force
```

Skill Installer 通常不会覆盖已存在目录。更新已有 skill 时，推荐先更新本地仓库，再复制覆盖 `%USERPROFILE%\.codex\skills\coco-*`。

更新完成后重新打开 Codex 会话，以加载最新技能描述。

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
