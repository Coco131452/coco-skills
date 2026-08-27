# 团队文档目录契约

`coco-docs-init` 与 `aile-docs-init` 使用同一目录和文件命名：

```text
docs/
├── README.md
├── specs/
│   ├── PRD.md
│   ├── SAD.md
│   └── CODEBASE-ANALYSIS.md
├── guides/
│   ├── AI-DEVELOPMENT-GUIDE.md
│   └── RUNBOOK.md
├── modules/
│   └── {module-name}.md
├── database/
│   ├── SCHEMA.md
│   └── MIGRATIONS.md
├── api/
│   └── api-spec.md
└── plans/
    └── {Work-Item-Key}/
```

## 模式 A：从需求创建

- 核心：`docs/README.md`、`docs/specs/PRD.md`、`docs/specs/SAD.md`、`docs/guides/AI-DEVELOPMENT-GUIDE.md`。
- 按实际范围：`docs/modules/*.md`、`docs/database/*.md`、`docs/api/api-spec.md`、`docs/guides/RUNBOOK.md`。
- `docs/plans/` 预留给后续需求和缺陷工作项。

## 模式 B：从代码回补

- 核心：模式 A 核心文件，加 `docs/specs/CODEBASE-ANALYSIS.md`。
- 有数据库实现时生成 `docs/database/SCHEMA.md` 和 `MIGRATIONS.md`。
- 有 API/CLI/RPC/Webhook/定时任务契约时生成 `docs/api/api-spec.md`。
- 每个核心模块生成 `docs/modules/{module-name}.md`。

只创建有事实内容的文件，不创建空占位文件。目录和文件名不得自行改名或放到其他位置。
