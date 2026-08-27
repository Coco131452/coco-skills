---
name: coco-delivery-report
description: 在需求或缺陷完成后生成可审查的交付摘要、验证结果、变更影响、部署说明和残余风险；仅在明确授权时执行外部同步。
---

# Coco 团队交付报告

只有分析/设计基线、计划状态、代码审查和验证结果一致时才报告完成。不得隐藏失败、跳过项或人工测试中尚未关闭的问题。

## 前置检查

- `analysis.md` 或 `defect-analysis.md` 指向当前有效基线。
- 所有已接受变更已进入相关文档，L0 待议事项单独列出。
- 计划任务完成或明确标记 `Superseded`、`Cancelled`、`Blocked`。
- P0/P1 审查问题已解决。
- 验收标准具有运行证据；Partial/Blocked 已说明风险。
- 若来源为 Jira，报告引用对应 Issue Key；若涉及 Server/API，已完成 Apifox 契约一致性验证。
- 已检查 `docs/README.md`、`docs/specs/{PRD,SAD,CODEBASE-ANALYSIS}.md`、`docs/guides/{AI-DEVELOPMENT-GUIDE,RUNBOOK}.md`、受影响的 `docs/modules/*.md`、`docs/database/*.md` 和 `docs/api/api-spec.md`；需要更新的已同步，不适用项已在 `verification.md` 说明原因。
- G3 代码审查已通过，G4 验收责任人已确认，或明确记录 `Partial`/`Blocked` 及批准的残余风险。

## 报告内容

按需更新 `docs/plans/{Work-Item-Key}/acceptance.md`，包括：

- 工作项目标与最终范围
- 主要实现和设计决定
- 变更文件/模块、公开契约和数据影响
- 验收标准及验证结果摘要
- 部署、Migration、配置、监控和回滚说明
- 已知限制、残余风险和后续工作
- 相关分析、设计、计划、变更和证据链接

面向 PR 的说明必须写入 `docs/plans/{Work-Item-Key}/pr-description.md`，使用 [PR 描述模板](references/pr-description-template.md)，包含 What、Why、Scope、Risk、Verification、Rollback、Jira 和设计/计划引用，不复制整份文档。

## 权限边界

生成本地报告不代表可以提交、推送、创建 PR、更新 Jira 工单、修改 Apifox 接口或部署。只有用户明确要求相应外部操作时执行，并在操作前确认目标仓库、Issue、接口项目、分支、环境和范围。

## 输出规范

只输出完成任务所需的核心内容；删除客套话、长篇铺垫、重复信息和无关说明。代码、文档和注释保持最小必要范围，不添加冗余注释。需要报告时优先给出结论、变更、验证结果和阻塞项。
