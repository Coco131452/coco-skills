# product-design.md 契约

路径：`docs/plans/{Work-Item-Key}/product-design.md`

```markdown
# 产品设计

## 1. 原型与设计来源
- Prototype：`prototype.html`
- Pencil：`design.pen` / Not Applicable
- Jira：Issue Key、Issue Type、链接

## 2. 页面与入口
## 3. 页面状态机
## 4. 条件判断与分支
| 场景 | 条件 | 页面行为 | 下一状态 | 验收标准 |
## 5. 接口触发流程
| 页面/动作 | 触发时机 | 接口名称 | Loading | Success | Empty | Error/权限 | 重试/恢复 |
## 6. 主流程、失败回路与返回路径
## 7. 响应式与可访问性
## 8. G2 确认记录
```

页面逻辑必须覆盖适用的加载、空、成功、失败、权限和恢复状态；接口路径、方法、参数、响应和错误码引用 `technical-design.md` 的接口调用清单。
