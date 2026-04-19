---
name: native-debugger
description: Debug native C, C++, Rust, and other compiled runtime problems using gdb or lldb. Use this for crashes, corrupted output, dangling pointers, invalid object state, stale callsites, memory errors, and lifetime bugs.
metadata:
  execution_mode: default-execute
  helper_mode: optional-python-helpers
  question_style: evidence-confirmation-only
---

# Native Debugger Skill

## Purpose

- C
- C++
- Rust in native-debug workflows
- native extension crashes
- corrupted runtime state
- memory and lifetime bugs


## Mandatory Start Rule

When this skill is invoked, do not begin with generic intake questions.

Treat the skill invocation itself as permission to:
1. inspect the repository
2. detect the toolchain
3. find likely entrypoints
4. attempt the smallest safe reproduction
5. collect initial runtime evidence

Only ask follow-up questions after this first local pass.

Do not ask for:
- programming language
- build tool
- code location
- error logs
- reproduction steps

if they can be inferred from the repository, current directory, build files, recent output, or the selected skill itself.

## Forbidden Opening Pattern

Do not open with questionnaire-style prompts such as:
- What language is this?
- What error are you seeing?
- How do I reproduce it?
- Which file is broken?
- Please provide logs first.

These questions are forbidden as the first response when repository inspection is possible.

## Minimal User Prompt Handling

Short user prompts such as:
- fix this
- result is wrong
- debug this
- this output is incorrect

must be treated as sufficient authorization to begin repository inspection and reproduction.

Do not require the user to restate information that can be discovered locally.

## Follow-up Question Style

Questions are allowed only after local inspection or execution.

Preferred question form:
- I detected X and observed Y. Is Y the incorrect behavior you want fixed?
- I reproduced the issue in file A or path B. Is this the same failure you care about?
- I found two plausible failure boundaries. Which one matches your expectation?

Do not ask open-ended intake questions before taking local action.

## Question Budget

After the first local pass, ask at most 2 focused questions at a time.
Each question must be tied to observed evidence.
Never ask a full intake questionnaire.

## Response Discipline

- Do not restate the entire skill description.
- Do not echo the workflow unless explicitly asked.
- Keep narration short.
- Prefer action over explanation.
- Prefer evidence over speculation.

## Skill Selection Implies Context

If this debugger skill is selected, assume the problem belongs to this language or runtime family unless the repository clearly disproves it.
Do not ask the user for the programming language as an opening move.
Infer it from:
- selected skill
- file extensions
- build files
- repository structure

## First Response Checklist

The first response after skill activation should do the following, in order:
1. inspect build files
2. inspect likely entrypoints or failing tests
3. infer the build or run command
4. run the smallest safe reproduction
5. summarize observed behavior
6. only then ask a narrow confirmation question if needed

The first response should not be a questionnaire.

## Helper Resolution Rules

Preferred helper lookup order:
1. `../python-helpers/`
2. `./python-helpers/`
3. `.opencode/python-helpers/`
4. `.claude/python-helpers/`
5. `.agents/python-helpers/`

If helpers are present, use them for repetitive procedural work.
If helpers are missing, do not stop. Fall back to shell inspection, repo-native commands, or inline Python.
Missing helpers are never fatal.

## Workspace Protection

Before editing:
- inspect workspace state if possible
- identify the exact files to be changed
- prefer minimal scoped edits
- snapshot files before non-trivial edits

After editing:
- rerun the minimal reproduction or validation
- if the change makes the situation worse, restore immediately

Never continue debugging on top of an unvalidated broken edit.
Never leave the user's code in a worse state.

## Toolchain Detection Rules

Do not ask which build tool to use if the repository already reveals it.
Prefer the repository's native workflow over inventing a new one.

## Python Helper Usage Policy

Use Python helpers for:
- toolchain detection
- entrypoint detection
- Python environment detection
- reproduction execution
- workspace snapshot and restore

Keep reasoning in the skill. Move repetitive procedure into helpers.

## Evidence Standard

Static reading may form hypotheses, but final root-cause claims must be backed by runtime evidence whenever runtime reproduction is available.


## Initial Scan Strategy

Look for build files such as `xmake.lua`, `CMakeLists.txt`, `Makefile`, `meson.build`, `Cargo.toml`, then locate the smallest likely entrypoint or failing test. Prefer a debug build with symbols. Use helpers when present; otherwise inspect the repo directly.

## Core Workflow

1. identify the symptom
2. reproduce the issue
3. locate the real entrypoint
4. build the execution path
5. inspect the relevant contract or boundary
6. collect runtime evidence
7. identify the first divergence
8. state the root cause
9. propose the narrowest correct fix
10. validate the fix

## Issue Framing Output

    issue_framing:
      symptom:
      failure_type:
      reproducer:
      entrypoint_hint:
      module_hint:
      suspected_contract:
      confidence:

Common `failure_type` values:
- crash
- segfault
- abort
- wrong_output
- stale_call_site
- bad_object_state
- ownership_error
- lifetime_error
- memory_error
- unknown

## Runtime Evidence Output

    runtime_evidence:
      stack:
      key_frames:
      args:
      locals:
      object_state:
      pointers:
      conditions:
      errors:

## Fix Guidance

- restore ownership or lifetime discipline
- refresh or re-acquire invalidated references or pointers
- repair caller and callee contract together
- restore invariants at the first wrong boundary
- revert speculative edits immediately if validation fails
