# technical-design.md 契约

路径：`docs/plans/{Work-Item-Key}/technical-design.md`

```markdown
# 技术设计

## 1. Jira 与 Apifox 来源
## 2. 架构与数据流
## 3. 接口调用清单
| 页面/模块 | 生成方法 | 调用文件 | HTTP 方法 | 路径 | 参数/请求体 | 响应模型 | 错误处理 | Apifox 引用 |
## 4. 当前契约与建议变更
## 5. 数据、权限与安全
## 6. Migration、兼容与回滚
## 7. 可观测性与验证策略
## 8. 技术决策
```

每个前端生成方法必须映射到一个已读取的 Apifox 契约；契约缺失或冲突时标记阻塞，不得猜测。
