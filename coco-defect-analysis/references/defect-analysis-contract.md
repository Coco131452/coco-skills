# defect-analysis.md 契约

路径：`docs/plans/{Bug-Key}/defect-analysis.md`

```markdown
# 缺陷分析

## 文档信息
- Work Item：
- 类型：Defect
- Jira Issue Type：Bug / Defect / Not Applicable
- 状态：Investigating / Confirmed / Superseded
- 来源：Jira / 人工测试 / 监控 / 用户反馈
- 创建时间：
- 更新时间：

## 1. Jira 缺陷理解摘要
## 2. 问题现象
## 3. 预期行为与实际行为
## 4. 环境与复现条件
## 5. 复现步骤和证据
## 6. Jira 与 Apifox 信息
## 7. 声明、契约、实现与实际行为差异
## 8. 根因分析
### 已验证事实
### 候选假设与排除证据
### 直接原因
### 根本原因
### 促成因素
## 9. 修改方案
### 推荐方案
### 备选方案
### 风险与回滚
## 10. 改动影响矩阵
| 范围 | 直接影响 | 间接影响 | 证据 |
## 11. 功能影响范围
## 12. 测试范围
## 13. 测试影响矩阵
| 测试层级 | 场景 | 必要性 | 验证方式 |
## 14. 修复范围与非修复范围
## 15. 待确认项
```

无法证明的根因必须保持为假设；只有 `Confirmed` 的缺陷分析才进入正式修复计划。
