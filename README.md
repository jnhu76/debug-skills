# Debug Skills Collection

[中文文档](README.zh.md)

A set of debugging skills that teach AI agents how to systematically diagnose and fix runtime bugs across five language families.

## What This Does

When you tell your AI agent "this produces wrong output" or "this crashes," the typical response is a lot of guessing. These skills give the agent a structured debugging workflow instead:

1. **Auto-detect** the project's language, build tool, and entry point
2. **Reproduce** the issue by running the smallest possible command
3. **Trace** the execution path and collect runtime evidence (stack, locals, object state)
4. **Identify** the first point where behavior diverges from expectation
5. **Propose** the narrowest fix and validate it by re-running

The agent does all of this without asking you a questionnaire upfront. It inspects the repo first, then asks at most 2 focused questions tied to evidence it has already observed.

## Supported Languages

| Skill | Languages | Typical Issues |
|-------|-----------|---------------|
| `python-debugger` | Python | Tracebacks, wrong output, object shape drift, async flow errors, import confusion |
| `jvm-debugger` | Java, Kotlin | Exceptions, transaction boundary errors, deadlocks, heap pressure, Spring proxy confusion |
| `node-debugger` | JavaScript (Node.js) | Promise chain errors, async ordering bugs, closure state leaks, event loop issues |
| `go-debugger` | Go | Panic analysis, interface-nil traps, goroutine coordination, channel protocol errors |
| `native-debugger` | C, C++, Rust | Segfaults, dangling pointers, memory corruption, lifetime errors, ownership violations |

## How It Works

Each skill is a `SKILL.md` file that defines a 10-step debugging workflow:

```
Identify symptom -> Reproduce -> Locate entrypoint -> Trace execution path ->
Inspect contract -> Collect evidence -> Find first divergence ->
State root cause -> Propose minimal fix -> Validate fix
```

Skills are **agent-neutral**: they work with any AI agent that can read markdown instructions (OpenCode, Claude Code, Cursor, etc.). No API keys, no plugins, no build step.

Helper scripts in `python-helpers/` automate repetitive tasks (toolchain detection, entrypoint detection, reproduction capture, workspace snapshots). Skills invoke them automatically when available, and fall back to shell commands when not. Missing helpers never block the workflow.

## Install

```bash
# OpenCode
cp -r *-debugger .opencode/skills/
cp -r python-helpers .opencode/

# Claude Code
cp -r *-debugger ~/.claude/skills/
cp -r python-helpers ~/.claude/

# Any agent with a skills directory
cp -r *-debugger <agent-skills-dir>/
cp -r python-helpers <agent-root>/
```

Install just one language if you don't need all five:

```bash
cp -r go-debugger .opencode/skills/
cp -r python-helpers .opencode/
```

Requirements: Python 3.8+ (for helper scripts only; the skills themselves are pure markdown).

## Use

Once installed, describe the problem to your agent in plain language:

```
fix this
debug this
result is wrong
this segfaults on startup
the Python script gives wrong output
```

The agent will:
- Detect the language and toolchain from the repo
- Run the smallest safe reproduction
- Ask at most 2 narrow questions (tied to evidence already observed)
- Propose a minimal fix and re-run to validate

You don't need to mention skill names, paste logs, or specify which file is broken.

## Try It Out

The repo includes ready-made practice projects in `examples/`. Each one compiles and runs successfully but produces **wrong output** -- perfect for testing whether the skill actually works.

```bash
git clone <repo-url> && cd debug-skills
```

Pick any example, cd into it, and ask your agent to debug:

```bash
cd examples/go-detached-pointer
# then tell your agent: "the stored balance should be 3000 but it's 2000, fix this"
```

### Available Examples

| Example | Language | Bug | Symptom |
|---------|----------|-----|---------|
| `python-late-bound-rules` | Python | Late-bound closure capture | bob gets `0` bonus instead of `100` |
| `java-detached-account` | Java | Detached object reference | Store balance stuck at `2000` instead of `3000` |
| `go-detached-pointer` | Go | Stale slice pointer after reallocation | Store balance stuck at `2000` instead of `3000` |
| `node-shared-state` | Node.js | Shared reference via `Array.fill` | All customers show the same order total |
| `cpp-detached-account` | C++ | Dangling pointer after container reload | Undefined behavior (use-after-free) |

Each example includes a `README.md` with the run command and expected vs actual output.

## Project Structure

```
debug-skills/
├── python-debugger/SKILL.md        # Python debugging skill
├── jvm-debugger/SKILL.md           # Java / Kotlin debugging skill
├── node-debugger/SKILL.md          # Node.js debugging skill
├── go-debugger/SKILL.md            # Go debugging skill
├── native-debugger/SKILL.md        # C / C++ / Rust debugging skill
├── python-helpers/                 # Helper scripts (invoked by skills, not by humans)
│   ├── detect_toolchain.py         #   Detect build tool from marker files
│   ├── detect_entrypoint.py        #   Find likely entry points
│   ├── detect_python_env.py        #   Detect Python virtual environment
│   ├── run_repro.py                #   Run reproduction command with output capture
│   └── workspace_guard.py          #   Snapshot and restore files for safe editing
├── manifest.json                   # Machine-readable collection metadata
├── VERSION                         # Current version
└── LICENSE                         # MIT
```

## License

MIT
