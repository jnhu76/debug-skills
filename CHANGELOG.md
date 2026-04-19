# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-04-19

### Added

- Initial stable release of Debug Skills Collection v3
- Five debugger skills covering Python, JVM, Node.js, Go, and Native (C/C++/Rust)
- Standardized 10-step debugging workflow across all skills
- Shared Python helper utilities (`python-helpers/`) for toolchain detection, entrypoint detection, environment detection, reproduction execution, and workspace protection
- Default execution policy: agents act first from repo evidence, ask only after local analysis
- Workspace protection with snapshot and restore capabilities
- Evidence-driven debugging: static hypotheses validated by runtime evidence
- Agent-neutral design: works with OpenCode, Claude, and any skill-supporting agent
- Helper resolution with 5-path fallback (skill sibling -> current dir -> .opencode -> .claude -> .agents)
- `manifest.json` for programmatic skill collection metadata

### Skills

#### python-debugger
- Debug Python runtime bugs using pdb or ipdb
- Handle tracebacks, wrong output, object/dict shape drift
- Address async flow errors, import confusion, monkey-patch side effects
- Failure types: `runtime_error`, `wrong_output`, `shape_mismatch`, `import_error`, `stale_call_site`, `async_flow_error`, `bad_default`, `monkey_patch_side_effect`

#### jvm-debugger
- Debug Java and Kotlin JVM services
- Use IDE debuggers, jdb, jstack, and jmap
- Handle exceptions, transaction boundary errors, deadlocks, heap pressure, Spring proxy issues
- Failure types: `runtime_exception`, `wrong_output`, `stale_call_site`, `transaction_boundary_error`, `thread_issue`, `deadlock`, `wiring_error`, `proxy_behavior_error`, `heap_behavior_issue`

#### node-debugger
- Debug Node.js runtime behavior using node inspect or IDE debuggers
- Handle async flow problems, promise chain issues, closure state bugs
- Address event loop issues and runtime shape drift
- Failure types: `runtime_exception`, `wrong_output`, `async_order_issue`, `promise_chain_error`, `stale_call_site`, `shape_mismatch`, `closure_state_issue`, `bad_default`

#### go-debugger
- Debug Go services, workers, tests, and CLIs using Delve
- Handle panic analysis, interface-nil traps
- Address channel behavior and goroutine coordination issues
- Failure types: `panic`, `wrong_output`, `stale_call_site`, `interface_nil_trap`, `shape_mismatch`, `goroutine_order_issue`, `channel_behavior_error`, `bad_default`

#### native-debugger
- Debug C, C++, Rust, and other compiled runtime problems using gdb or lldb
- Handle crashes, segfaults, dangling pointers, memory errors, lifetime bugs
- Address corrupted object state and ownership errors
- Failure types: `crash`, `segfault`, `abort`, `wrong_output`, `stale_call_site`, `bad_object_state`, `ownership_error`, `lifetime_error`, `memory_error`

### Python Helpers

- **detect_toolchain.py**: Detect project toolchain (xmake, cmake, make, meson, cargo, go, python, node, maven, gradle)
- **detect_entrypoint.py**: Detect project entry points (main.cpp, main.py, main.go, index.js, etc.)
- **detect_python_env.py**: Detect Python virtual environments and dependencies
- **run_repro.py**: Run reproduction commands with configurable timeout and structured output capture
- **workspace_guard.py**: Workspace snapshot and restore for safe editing with rollback

### Examples

Five practice bug projects in `examples/`:

| Example | Language | Bug Pattern | Symptom |
|---------|----------|-------------|---------|
| `python-late-bound-rules` | Python | Late-bound closure capture | `bob=0, carol=600` instead of `bob=100, carol=400` |
| `java-detached-account` | Java | Detached object reference | Store balance `2000` instead of `3000` |
| `go-detached-pointer` | Go | Stale slice pointer | Store balance `2000` instead of `3000` |
| `node-shared-state` | Node.js | Shared reference via `Array.fill` | All customers show `monthlyTotal=250` |
| `cpp-detached-account` | C++ | Dangling pointer after container reload | Undefined behavior (use-after-free) |

All example runtime outputs are collected in `examples/RUN_OUTPUTS.txt`.

### Design Principles

1. **Default to execution, not questionnaires**: Infer from available evidence first
2. **Ask only after an initial local pass**: Gather context before asking questions
3. **Respect native toolchains**: Detect and use the project's existing workflow
4. **Snapshot before edits**: Protect workspace state before non-trivial changes
5. **Use evidence over speculation**: Runtime reproduction validates root causes
6. **Agent-neutral**: Work across different AI agent implementations

---

## Release Notes Template

When releasing a new version, copy this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```
