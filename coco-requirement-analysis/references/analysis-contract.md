# analysis.md 契约

路径：`docs/plans/{Story-Key}/analysis.md`

```markdown
# 需求分析

## 文档信息
- Work Item：
- 类型：Requirement
- Jira Issue Type：Story / Task / Epic / Not Applicable
- 状态：Draft / Confirmed / Superseded
- 来源：Jira / 用户说明 / 项目文档 / 代码推导
- UI 设计状态：Required / Reuse Existing / Not Applicable / Provisional
- 创建时间：
- 更新时间：

## 1. Jira 需求理解摘要
## 2. 背景与目标
## 3. 用户角色与使用场景
## 4. 用户故事
## 5. 验收标准
## 6. 功能范围
### 包含
### 不包含
## 7. 优先级与依赖
## 8. 非功能需求
## 9. 现有代码与影响范围
## 9.1 UI 设计判断与来源
## 10. 测试范围
## 11. Jira 与 Apifox 来源
## 11.1 前端接口范围与 Apifox 读取状态
## 12. 来源差异
## 13. 风险、假设与待确认项
## 14. 需求追踪表
| Story | 功能模块 | 验收标准 | 测试范围 |
```

用户故事使用稳定 ID，例如 `US-001`；验收标准使用 `AC-001`。前端需求必须记录 UI 设计状态及原型、参考页面或设计系统来源；未确认时使用 `Provisional`。代码推导和其他未确认内容必须标明来源或 `Provisional`；`Confirmed` 后才可作为正式计划基线。
