# Contributing Guide

Thank you for your interest in contributing to Debug Skills Collection! This document covers how to contribute to this multi-language debugging skill collection.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Adding a New Debugger Skill](#adding-a-new-debugger-skill)
- [Improving an Existing Skill](#improving-an-existing-skill)
- [Adding Examples](#adding-examples)
- [Python Helper Contributions](#python-helper-contributions)
- [Commit Convention](#commit-convention)
- [Code Review](#code-review)

## Code of Conduct

- Be respectful to all participants
- Accept constructive criticism
- Focus on what is best for the community

## How to Contribute

### Reporting Bugs

If you find a bug, create an issue including:

1. **Environment information**
   - OS and version
   - Programming language and version
   - Relevant toolchain version

2. **Reproduction steps**
   - Clear step-by-step instructions
   - Minimal reproducible example

3. **Expected vs actual behavior**
   - What you expected to happen
   - What actually happened

4. **Relevant logs or output**
   - Error messages
   - Stack traces
   - Relevant log snippets

### Suggesting New Features

For feature suggestions:

1. Check if a similar issue already exists
2. Describe the use case clearly
3. Explain why this feature adds value to the project
4. Provide implementation ideas or pseudocode if possible

## Adding a New Debugger Skill

To add support for a new programming language or runtime:

### 1. Directory Structure

Create a new skill directory:

```
<language>-debugger/
├── SKILL.md
└── python-helpers/        # Copy of shared helpers
    ├── detect_toolchain.py
    ├── detect_entrypoint.py
    ├── detect_python_env.py
    ├── run_repro.py
    └── workspace_guard.py
```

### 2. SKILL.md Structure

Every `SKILL.md` must include the following sections. Use existing skills as templates.

#### Frontmatter

```yaml
---
name: <language>-debugger
description: Short description of the skill's purpose and applicable scenarios
metadata:
  execution_mode: default-execute
  helper_mode: optional-python-helpers
  question_style: evidence-confirmation-only
---
```

#### Required Sections

All skills must include these standard sections (copy from an existing skill):

| Section | Purpose |
|---------|---------|
| **Purpose** | List applicable problem types for this language |
| **Mandatory Start Rule** | Defines the "act first, ask later" policy |
| **Forbidden Opening Pattern** | Lists disallowed questionnaire-style openings |
| **Minimal User Prompt Handling** | How to handle short prompts like "fix this" |
| **Follow-up Question Style** | Evidence-tied question format |
| **Question Budget** | Max 2 focused questions after local pass |
| **Response Discipline** | Prefer action over explanation |
| **Skill Selection Implies Context** | Infer language from skill/file extensions |
| **First Response Checklist** | 6-step ordered first response |
| **Helper Resolution Rules** | 5-path helper lookup order |
| **Workspace Protection** | Snapshot before edit, restore on failure |
| **Toolchain Detection Rules** | Auto-detect from repo markers |
| **Python Helper Usage Policy** | What to use helpers for |
| **Evidence Standard** | Runtime evidence required for root cause claims |

#### Language-Specific Sections

Customize these per language:

| Section | What to Customize |
|---------|-------------------|
| **Initial Scan Strategy** | Which marker files to look for |
| **Core Workflow** | The standard 10-step flow (same for all) |
| **Issue Framing Output** | `failure_type` enum values specific to this language |
| **Runtime Evidence Output** | Language-specific state fields |
| **Fix Guidance** | Language-specific fix best practices |

### 3. failure_type Values by Language

Reference for existing languages:

| Skill | failure_type values |
|-------|-------------------|
| `python-debugger` | `runtime_error`, `wrong_output`, `shape_mismatch`, `import_error`, `stale_call_site`, `async_flow_error`, `bad_default`, `monkey_patch_side_effect` |
| `jvm-debugger` | `runtime_exception`, `wrong_output`, `stale_call_site`, `transaction_boundary_error`, `thread_issue`, `deadlock`, `wiring_error`, `proxy_behavior_error`, `heap_behavior_issue` |
| `node-debugger` | `runtime_exception`, `wrong_output`, `async_order_issue`, `promise_chain_error`, `stale_call_site`, `shape_mismatch`, `closure_state_issue`, `bad_default` |
| `go-debugger` | `panic`, `wrong_output`, `stale_call_site`, `interface_nil_trap`, `shape_mismatch`, `goroutine_order_issue`, `channel_behavior_error`, `bad_default` |
| `native-debugger` | `crash`, `segfault`, `abort`, `wrong_output`, `stale_call_site`, `bad_object_state`, `ownership_error`, `lifetime_error`, `memory_error` |

All skills also include `unknown` as a fallback.

### 4. Copy Python Helpers

Each skill directory must include a copy of `python-helpers/` so the skill can function standalone:

```bash
cp -r python-helpers/ <language>-debugger/python-helpers/
```

## Improving an Existing Skill

### Documentation Improvements

1. Fork the repository
2. Create a feature branch (`git checkout -b improve/<skill-name>-docs`)
3. Edit the `SKILL.md`
4. Commit (`git commit -am 'Improve <skill> documentation'`)
5. Push (`git push origin improve/<skill-name>-docs`)
6. Open a Pull Request

### Logic Fixes

1. Create an issue to discuss the problem first
2. Reach consensus before starting work
3. Follow the PR workflow above

## Adding Examples

Practice examples are small, self-contained projects that demonstrate a specific bug pattern. Each example should:

1. **Run successfully** (no syntax errors, no compile errors)
2. **Produce wrong output** (the bug is in behavior, not syntax)
3. **Require runtime reasoning** (not solvable by static grep alone)

### Example Structure

```
examples/<example-name>/
├── README.md          # Run command, intended vs actual behavior
├── <source files>     # Runnable source code
└── (optional build files)
```

### Example README Template

```markdown
# <example-name>

## Run

\```bash
<command to build and run>
\```

## Intended behavior

<What should happen>

## Actual behavior

<What actually happens - include the wrong output>
```

### Existing Examples

| Example | Language | Bug Pattern |
|---------|----------|-------------|
| `python-late-bound-rules` | Python | Late-bound closure variable capture |
| `java-detached-account` | Java | Detached object reference after reload |
| `go-detached-pointer` | Go | Stale slice pointer after reallocation |
| `node-shared-state` | Node.js | Shared object reference via `Array.fill` |
| `cpp-detached-account` | C++ | Dangling pointer after container reload |

## Python Helper Contributions

### Adding a New Helper

1. Create a new `.py` file in `python-helpers/`
2. Add shebang (`#!/usr/bin/env python3`)
3. Output results as JSON
4. Add a docstring explaining the purpose
5. Update `README.md` helper list
6. Copy the new helper to all skill directories that include `python-helpers/`

### Improving Existing Helpers

- Maintain backward compatibility when possible
- Update related documentation
- Ensure changes are reflected across all copies in skill directories

## Commit Convention

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code meaning change)
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Build or helper tooling changes

Example:
```
feat: add rust-debugger skill for Rust debugging

- Add SKILL.md with standard 10-step workflow
- Include Rust-specific failure types
- Add ownership/lifetime fix guidance
- Copy python-helpers to rust-debugger/
```

### Branch Naming

- `feat/<name>` - New features
- `fix/<name>` - Bug fixes
- `docs/<name>` - Documentation
- `improve/<skill>-<aspect>` - Improvements to existing skill

## Code Review

All contributions require review. Reviewers check:

- Adherence to project design principles
- Documentation clarity and completeness
- Standard workflow compliance
- Inclusion of all required SKILL.md sections
- Python helpers copied to the new skill directory
- Examples follow the established pattern

## Getting Help

1. Read existing skills as reference
2. Check the [README.md](README.md) for background
3. Create an issue tagged `question`
4. Discuss in the relevant issue or PR

Thank you for contributing!
