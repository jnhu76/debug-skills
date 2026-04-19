# Debug Skills Collection v3

A generic, agent-neutral multi-language debugging skill collection supporting Python, JVM (Java/Kotlin), Node.js, Go, and Native (C/C++/Rust) programs.

## Table of Contents

- [Project Goals](#project-goals)
- [Supported Languages and Scenarios](#supported-languages-and-scenarios)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Python Helpers](#python-helpers)
- [Design Principles](#design-principles)
- [License](#license)
- [Contributing](#contributing)

## Project Goals

Debug Skills Collection provides AI agents with a standardized, reusable set of debugging capabilities:

1. **Default to Execution** - Infer from available evidence first, ask questions only when needed
2. **Environment-Aware** - Auto-detect project toolchain and runtime environment
3. **Minimal Interference** - Prefer the smallest scoped edit that fixes the issue
4. **Evidence-Driven** - Static analysis forms hypotheses; runtime evidence validates root causes
5. **Agent-Neutral** - No dependency on a specific agent or shell

## Supported Languages and Scenarios

| Language/Platform | Skill Name | Applicable Scenarios |
|-----------|-----------|---------|
| Python | `python-debugger` | Runtime errors, tracebacks, wrong output, object shape drift, async issues, import confusion |
| JVM (Java/Kotlin) | `jvm-debugger` | Exceptions, transaction issues, thread problems, heap pressure, framework boundary bugs, Spring proxy issues |
| Node.js | `node-debugger` | Wrong output, exceptions, async flow problems, promise chain issues, closure state bugs, event loop issues |
| Go | `go-debugger` | Panic analysis, wrong output, goroutine issues, channel behavior, interface-nil traps |
| Native (C/C++/Rust) | `native-debugger` | Crashes, segfaults, wrong output, dangling pointers, corrupted object state, memory errors, lifetime bugs |

## Project Structure

```
debug-skills/
├── README.md                      # This file - project overview
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guidelines
├── LICENSE                        # MIT License
├── VERSION                        # Current version (3.0.0)
├── manifest.json                  # Skill collection manifest
│
├── python-helpers/                # Shared Python helper scripts
│   ├── detect_toolchain.py        # Detect project toolchain (xmake, cmake, make, meson, cargo, go, python, node, maven, gradle)
│   ├── detect_entrypoint.py       # Detect project entry points
│   ├── detect_python_env.py       # Detect Python environment
│   ├── run_repro.py               # Run reproduction commands with timeout and output capture
│   └── workspace_guard.py         # Workspace snapshot and restore
│
├── python-debugger/               # Python debugging skill
│   ├── SKILL.md
│   └── python-helpers/            # Symlinked / copied helpers
│
├── jvm-debugger/                  # JVM debugging skill (Java/Kotlin)
│   ├── SKILL.md
│   └── python-helpers/
│
├── node-debugger/                 # Node.js debugging skill
│   ├── SKILL.md
│   └── python-helpers/
│
├── go-debugger/                   # Go debugging skill
│   ├── SKILL.md
│   └── python-helpers/
│
├── native-debugger/               # Native debugging skill (C/C++/Rust)
│   ├── SKILL.md
│   └── python-helpers/
│
└── examples/                      # Practice bug projects
    ├── README.md
    ├── RUN_OUTPUTS.txt            # Collected runtime outputs
    ├── python-late-bound-rules/   # Late-bound closure bug
    ├── java-detached-account/     # Detached object reference bug
    ├── go-detached-pointer/       # Stale slice pointer bug
    ├── node-shared-state/         # Shared reference state bug
    └── cpp-detached-account/      # Dangling pointer after reload
```

## Installation

### OpenCode

Copy skill directories to `.opencode/skills/` and helpers to `.opencode/python-helpers/`:

```bash
cp -r python-debugger jvm-debugger node-debugger go-debugger native-debugger .opencode/skills/
cp -r python-helpers .opencode/
```

### Claude / Other Agents

Copy to the agent's skill root directory:

```bash
# Claude
cp -r python-debugger ~/.claude/skills/
cp -r python-helpers ~/.claude/

# Generic agents
cp -r python-debugger .agents/skills/
cp -r python-helpers .agents/
```

### Helper Resolution Order

Skills search for Python helpers in the following order:

1. `../python-helpers/` (sibling of skill directory)
2. `./python-helpers/` (current directory)
3. `.opencode/python-helpers/`
4. `.claude/python-helpers/`
5. `.agents/python-helpers/`

If helpers are not found, skills fall back to shell inspection, repo-native commands, or inline Python. Missing helpers are never fatal.

## Usage

### 1. Select the Right Skill

Choose based on the problem type and programming language:

- **Python issues** -> `python-debugger`
- **Java/Kotlin issues** -> `jvm-debugger`
- **Node.js issues** -> `node-debugger`
- **Go issues** -> `go-debugger`
- **C/C++/Rust issues** -> `native-debugger`

### 2. Invoke via Agent

In agents that support skills, reference directly:

```
Please use the python-debugger skill to analyze this traceback
```

Short prompts like `fix this`, `debug this`, or `result is wrong` are treated as sufficient authorization to begin inspection.

### 3. Core Workflow (Common to All Skills)

All debugger skills follow the same 10-step workflow:

```
1.  Identify the symptom
2.  Reproduce the issue
3.  Locate the real entrypoint
4.  Build the execution path
5.  Inspect the contract or boundary
6.  Collect runtime evidence
7.  Identify the first divergence
8.  State the root cause
9.  Propose the narrowest correct fix
10. Validate the fix
```

### 4. Issue Framing and Evidence

Each skill produces structured outputs:

**Issue Framing:**

```yaml
issue_framing:
  symptom: "Description of the observed problem"
  failure_type: "One of the skill-specific failure types"
  reproducer: "Command or steps to reproduce"
  entrypoint_hint: "Likely entry point"
  module_hint: "Suspected module"
  suspected_contract: "Contract or boundary under suspicion"
  confidence: "high / medium / low"
```

**Runtime Evidence:**

```yaml
runtime_evidence:
  stack: "Call stack"
  key_frames: "Key frames"
  args: "Arguments"
  locals: "Local variables"
  object_state: "Object state"
  errors: "Error messages"
```

Fields vary per language (e.g., `goroutines` and `channel_state` for Go, `thread_state` and `heap_state` for JVM).

## Examples

The `examples/` directory contains practice bug projects. Each project runs successfully but produces incorrect output. They are designed for debugger-skill practice rather than static grep-only reading.

### python-late-bound-rules

**Bug type:** Late-bound closure variable capture

```bash
cd examples/python-late-bound-rules && python main.py
```

`build_bonus_rules()` creates lambdas in a loop, but all lambdas capture the same `threshold` and `bonus` variables from the final iteration. Expected: `bob=100, carol=400`. Actual: `bob=0, carol=600`.

### java-detached-account

**Bug type:** Detached object reference

```bash
cd examples/java-detached-account && javac Main.java && java Main
```

After `reloadFromDisk()` replaces the internal list, the `focus` reference points to a detached `Account` object. Applying the VIP bonus modifies the stale object, not the one currently in the store. Expected store balance: `3000`. Actual: `2000`.

### go-detached-pointer

**Bug type:** Stale slice pointer after reallocation

```bash
cd examples/go-detached-pointer && go run .
```

`findByID()` returns a pointer into the internal slice. After `reloadFromDisk()` reassigns the slice, the old pointer becomes stale. `applyVIPBonus()` modifies the stale memory. Expected store balance: `3000`. Actual: `2000`.

### node-shared-state

**Bug type:** Shared object reference via `Array.fill`

```bash
cd examples/node-shared-state && node main.js
```

`Array(n).fill(baseSummary)` fills the array with references to the same object. Recording an order for one customer updates all customers. Expected: only `bob` has `monthlyTotal=250`. Actual: all customers show `250`.

### cpp-detached-account

**Bug type:** Dangling pointer after container reload

```bash
cd examples/cpp-detached-account && make && ./demo
```

`findById()` returns a raw pointer into the `unique_ptr` vector. After `reloadFromDisk()` clears and repopulates the vector, the old pointer is dangling. Applying the VIP bonus writes to freed memory. This is undefined behavior.

All example outputs are collected in [`examples/RUN_OUTPUTS.txt`](examples/RUN_OUTPUTS.txt).

## Python Helpers

The `python-helpers/` directory contains Python scripts designed to be invoked by skills during debugging sessions. They are **not intended for direct human use** -- skills dispatch them automatically at appropriate workflow stages (toolchain detection, reproduction, workspace protection, etc.).

When helpers are available on the [helper resolution path](#helper-resolution-order), skills use them for repetitive procedural work. When helpers are missing, skills fall back to shell inspection, repo-native commands, or inline Python. Missing helpers are never fatal.

### Helper Overview

| Script | Invoked When | Output |
|--------|-------------|--------|
| `detect_toolchain.py` | Skill needs to identify the build system | JSON with `primary` tool, `detected` markers, and `commands` map |
| `detect_entrypoint.py` | Skill needs to locate the program entry file | Likely entry paths (e.g. `main.cpp`, `main.py`, `app.py`, `index.js`) |
| `detect_python_env.py` | Skill needs to check Python venv or dependency state | Environment metadata |
| `run_repro.py` | Skill needs to reproduce the bug and capture output | JSON: `returncode`, `stdout`, `stderr`, `duration_sec` |
| `workspace_guard.py` | Skill is about to edit files (snapshot) or needs to rollback (restore) | Snapshot metadata / file restoration |

### Example: Toolchain Detection Output

When a skill invokes `detect_toolchain.py`, it receives structured JSON:

```json
{
  "cwd": "/home/user/my-project",
  "primary": "python",
  "detected": [
    {"tool": "python", "marker": "pyproject.toml", "paths": ["..."]},
    {"tool": "node", "marker": "package.json", "paths": ["..."]}
  ],
  "commands": {
    "build": "",
    "run": "python <entry.py>",
    "test": "pytest -q"
  }
}
```

Supported toolchains: xmake, cmake, make, meson, cargo, go, python, node, maven, gradle.

## Design Principles

### 1. Default to Execution, Not Questionnaires

Skills do not begin with generic intake questions. They:
- Infer from repository structure, build files, logs, and test output
- Ask only when information is insufficient to proceed
- Ask after the first local analysis pass, not before

### 2. Evidence Standard

- Static reading forms hypotheses
- Root cause claims require runtime evidence
- Runtime reproduction > static analysis

### 3. Environment-Aware Toolchain Detection

- Never ask which build tool to use if the repo reveals it
- Auto-detect toolchain from marker files
- Prefer the project's native workflow

### 4. Minimal Scoped Edits

- Identify exact files before editing
- Prefer the smallest change that fixes the issue
- Snapshot files before non-trivial edits
- Restore immediately if a change makes things worse

### 5. Agent-Neutral

- No dependency on a specific agent or shell
- Helpers fall back gracefully when missing
- Install into any agent that supports skills

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new debugger skills, improving existing ones, and contributing Python helpers.

---

**Version**: 3.0.0
**License**: MIT
**Author**: Debug Skills Team
