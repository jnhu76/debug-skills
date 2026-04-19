# Debug Skills Collection v3

A generic, agent-neutral multi-language debugging skill collection for Python, JVM (Java/Kotlin), Node.js, Go, and Native (C/C++/Rust).

## Install

```bash
# OpenCode
cp -r *-debugger .opencode/skills/
cp -r python-helpers .opencode/

# Claude
cp -r *-debugger ~/.claude/skills/
cp -r python-helpers ~/.claude/

# Any agent
cp -r *-debugger .agents/skills/
cp -r python-helpers .agents/
```

Or install just one language, e.g. `cp -r go-debugger .opencode/skills/`.

No config, no build step, no dependencies beyond Python 3.8+.

## Use

Once installed, just describe the problem to your agent:

```
fix this
debug this
result is wrong
this segfaults on startup
```

The agent loads the matching debugger skill, detects toolchain and entrypoint, reproduces the issue, and proposes a fix. No need to mention skill names or provide logs upfront.

## Skills

| Skill | Languages | Handles |
|-------|-----------|---------|
| `python-debugger` | Python | Runtime errors, tracebacks, shape drift, async bugs, import issues |
| `jvm-debugger` | Java, Kotlin | Exceptions, transaction errors, deadlocks, heap pressure, Spring proxy issues |
| `node-debugger` | JavaScript | Async flow, promise chains, closure state, event loop issues |
| `go-debugger` | Go | Panics, interface-nil traps, goroutine issues, channel behavior |
| `native-debugger` | C, C++, Rust | Crashes, segfaults, dangling pointers, memory errors, lifetime bugs |

## Project Structure

```
debug-skills/
├── python-debugger/SKILL.md
├── jvm-debugger/SKILL.md
├── node-debugger/SKILL.md
├── go-debugger/SKILL.md
├── native-debugger/SKILL.md
├── python-helpers/          # Auto-invoked by skills, not for human use
│   ├── detect_toolchain.py
│   ├── detect_entrypoint.py
│   ├── detect_python_env.py
│   ├── run_repro.py
│   └── workspace_guard.py
├── manifest.json
├── VERSION
└── LICENSE
```

## License

MIT
