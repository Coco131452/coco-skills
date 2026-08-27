---
name: coco-product-design
description: 为涉及界面或交互的需求设计用户流程，并优先生成可在浏览器预览的 HTML 原型。
---

# Coco 产品设计与原型协作

仅在工作项涉及 UI、交互或用户流程时使用。先读取需求基线、现有设计系统、相似页面和组件，优先延续项目既有模式。UI 工作项默认先生成 HTML 原型并进行浏览器预览；纯后端或无用户可见变化的工作项记录“不适用”即可。

## 原型流程

1. G1 需求确认后，固化页面边界、状态矩阵、主流程、失败回路和复用组件。
2. 生成 `docs/plans/{Work-Item-Key}/prototype.html`，使用静态或 mock 数据表达关键页面、状态和交互；原型不是生产代码。
3. 在真实浏览器中预览并检查主流程、异常态、响应式布局、控制台错误和关键交互；记录截图或运行证据。
4. 根据反馈迭代原型，直到产品/需求负责人确认效果。
5. 在 `analysis.md` 回填原型路径、预览环境、覆盖状态、证据和待实现差异。
6. G2 原型审查通过后，才进入 `coco-writing-plans` 和代码实现。

## 页面逻辑与接口流程

- 在 `product-design.md` 或 `analysis.md` 中补充页面状态机、条件判断、分支、接口触发时机、成功/空/加载/失败/权限状态、重试和返回路径。
- 每个页面逻辑分支必须回溯到用户故事、验收标准或 Jira 描述，并在 G2 由产品/需求负责人确认。
- 页面需要接口数据时，标记接口名称和调用时机；路径、方法、参数、响应和错误码以 Apifox 契约为准，由 `technical-design.md` 或 `plan.md` 登记。

## 可选 Pencil 设计

只有用户或设计团队明确要求可编辑 Pencil 设计稿时，才额外生成 `docs/plans/{Work-Item-Key}/design.pen`。此时 `design.pen` 与 `prototype.html` 必须保持范围和状态一致，并在 `analysis.md` 记录对应关系；不要求 Pencil 时不创建 `design.pen`。

## 设计内容

- 用户任务、入口、主路径、返回路径和导航关系。
- 信息层级、页面布局、组件职责和复用点。
- Loading、Empty、Error、Success、Disabled、Permission denied 等适用状态。
- 表单验证、危险操作确认、撤销/恢复和键盘操作。
- 桌面与移动布局、长文本、缩放和无障碍要求。
- 用户可见反馈、失败恢复及关键埋点。
- 与 API/数据能力有关但尚未确定的假设。

交互应针对实际业务场景，不加入无助于任务完成的装饰或说明文字。若存在参考设计，明确哪些必须保持，哪些允许调整。

## 产物

涉及 UI 时使用 `docs/plans/{Work-Item-Key}/prototype.html`；如需要文字补充，写入同目录的 `product-design.md`。若明确要求 Pencil，再按需创建 `design.pen`。若无 UI，必须在 `analysis.md` 写明原因。

创建或维护 `product-design.md` 前读取 [product-design-contract.md](references/product-design-contract.md)。

在 `plan.md` 或 `analysis.md` 登记原型/设计文件路径和版本。原型未确认时标记 `Provisional`，不得把原型自动视为最终需求。

## 输出规范

只输出完成任务所需的核心内容；删除客套话、长篇铺垫、重复信息和无关说明。代码、文档和注释保持最小必要范围，不添加冗余注释。需要报告时优先给出结论、变更、验证结果和阻塞项。
