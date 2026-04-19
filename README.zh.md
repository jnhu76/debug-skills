# Debug Skills Collection

[English](README.md)

一套调试技能，教 AI agent 如何系统性地诊断和修复运行时 bug，覆盖五种语言/平台。

## 这是什么

当你对 AI agent 说"输出不对"或"程序崩了"，通常得到的回答是瞎猜。这套技能给 agent 一个结构化的调试流程：

1. **自动检测**项目的语言、构建工具和入口点
2. **复现**问题，运行最小可复现命令
3. **追踪**执行路径，收集运行时证据（调用栈、局部变量、对象状态）
4. **定位**行为第一个偏离预期的位置
5. **提出**最小范围的修复方案，重新运行验证

Agent 不会一开始就问你一堆问题。它会先检查仓库，然后最多问 2 个有针对性的问题（基于已经观察到的证据）。

## 支持的语言

| 技能 | 语言 | 典型问题 |
|------|------|---------|
| `python-debugger` | Python | Traceback、输出错误、对象结构漂移、异步流程错误、导入混乱 |
| `jvm-debugger` | Java、Kotlin | 异常、事务边界错误、死锁、堆压力、Spring 代理混淆 |
| `node-debugger` | JavaScript (Node.js) | Promise 链错误、异步顺序 bug、闭包状态泄漏、事件循环问题 |
| `go-debugger` | Go | Panic 分析、interface-nil 陷阱、goroutine 协调问题、channel 协议错误 |
| `native-debugger` | C、C++、Rust | 段错误、悬空指针、内存损坏、生命周期错误、所有权违规 |

## 工作原理

每个技能是一个 `SKILL.md` 文件，定义了 10 步调试流程：

```
识别症状 -> 复现问题 -> 定位入口 -> 追踪执行路径 ->
检查合约/边界 -> 收集运行时证据 -> 找到第一个分歧点 ->
陈述根因 -> 提出最小修复 -> 验证修复
```

技能是 **Agent 无关的**：任何能读取 markdown 指令的 AI agent 都能用（OpenCode、Claude Code、Cursor 等）。不需要 API key、不需要插件、不需要构建。

`python-helpers/` 中的辅助脚本自动化重复性任务（工具链检测、入口点检测、复现命令执行、工作区快照）。技能会在可用时自动调用它们，不可用时回退到 shell 命令。辅助脚本缺失不会阻断流程。

## 安装

```bash
# OpenCode
cp -r *-debugger .opencode/skills/
cp -r python-helpers .opencode/

# Claude Code
cp -r *-debugger ~/.claude/skills/
cp -r python-helpers ~/.claude/

# 任何支持 skills 目录的 agent
cp -r *-debugger <agent-skills-dir>/
cp -r python-helpers <agent-root>/
```

只需要某一种语言也可以：

```bash
cp -r go-debugger .opencode/skills/
cp -r python-helpers .opencode/
```

要求：Python 3.8+（仅辅助脚本需要；技能本身是纯 markdown）。

## 使用

安装后，用自然语言描述问题即可：

```
fix this
debug this
result is wrong
this segfaults on startup
Python 脚本输出不对
```

Agent 会：
- 从仓库自动检测语言和工具链
- 运行最小安全复现
- 最多问 2 个聚焦的问题（基于已观察到的证据）
- 提出最小修复方案并重新运行验证

不需要提及技能名称、粘贴日志、或指定哪个文件出了问题。

## 项目结构

```
debug-skills/
├── python-debugger/SKILL.md        # Python 调试技能
├── jvm-debugger/SKILL.md           # Java / Kotlin 调试技能
├── node-debugger/SKILL.md          # Node.js 调试技能
├── go-debugger/SKILL.md            # Go 调试技能
├── native-debugger/SKILL.md        # C / C++ / Rust 调试技能
├── python-helpers/                 # 辅助脚本（由技能自动调用，非人工使用）
│   ├── detect_toolchain.py         #   从标记文件检测构建工具
│   ├── detect_entrypoint.py        #   查找可能的入口点
│   ├── detect_python_env.py        #   检测 Python 虚拟环境
│   ├── run_repro.py                #   运行复现命令并捕获输出
│   └── workspace_guard.py          #   文件快照与恢复，安全编辑
├── manifest.json                   # 机器可读的集合元数据
├── VERSION                         # 当前版本
└── LICENSE                         # MIT
```

## 许可证

MIT
