---
name: coco-codebase-index
description: 为软件项目建立、查询、验证和增量刷新本地代码索引，快速定位入口、符号、依赖、功能影响与测试范围；适用于需求分析、缺陷调查和修改前影响评估。
---

# Coco 代码库索引

索引用于导航和影响分析，不是代码事实来源。修改前必须打开相关实际文件确认；索引过期时先刷新。

## 命令

使用本技能目录下的 `scripts/codebase_index.py`：

```bash
python scripts/codebase_index.py initialize --root <repo>
python scripts/codebase_index.py refresh --root <repo>
python scripts/codebase_index.py validate --root <repo>
python scripts/codebase_index.py query <term> --root <repo>
python scripts/codebase_index.py impact <path> [<path>...] --root <repo>
```

- `initialize`：首次建立 `.coco/codebase-index/`。
- `refresh`：按路径、大小、修改时间和哈希复用未变文件，只重新解析变化文件。
- `validate`：比较当前文件与 manifest；过期时退出码为 2。
- `query`：按路径、符号和依赖搜索。
- `impact`：沿反向依赖列出直接/间接受影响文件和测试候选。

## 工作方式

1. 确认项目根目录和忽略规则。
2. 首次使用运行 `initialize`；已有索引先运行 `validate`，过期则 `refresh`。
3. 需求分析查询相似功能、入口、模块和现有测试。
4. 缺陷分析从失败入口执行 `impact`，再用实际代码确认调用链和共享调用方。
5. 代码完成后刷新索引，并在交付报告中记录索引状态。

## 安全与限制

- 默认排除 `.git`、依赖、构建产物、缓存、`.coco` 和常见 IDE 目录。
- 不读取 `.env`、凭据、密钥、证书或二进制文件。
- 正则符号/依赖提取是轻量导航，不等同编译器语义分析；动态导入、反射、生成代码和运行时注册需人工验证。
- 不因索引结果自动修改代码，也不把“未找到”解释为“不存在”。

输出包括 `manifest.json`、`files.jsonl`、`symbols.jsonl`、`dependencies.jsonl`、`entrypoints.jsonl`、`test-map.jsonl`、`project-summary.md` 和 `index-state.json`。
