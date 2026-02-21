# AGENTS.md

This file defines working standards for contributors and coding agents in this repository.

## Scope

- Applies to the entire repository.
- Prioritize safety and reliability over speed when hardware is connected.

## Commit Best Practices

- Make small, atomic commits with one clear purpose.
- Use imperative commit messages:
  - `feat: add AX-12 scan helper`
  - `fix: validate goal position bounds`
  - `docs: add serial troubleshooting notes`
- Recommended commit format:
  - `<type>: <short summary>`
  - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
- Include rationale in the commit body when behavior changes.
- Never commit secrets, local serial paths, or machine-specific credentials.
- Do not mix formatting-only edits with functional changes in one commit.
- Before committing, run:
  - Syntax checks
  - Relevant tests
  - Example scripts (with hardware disconnected or mocked unless explicitly testing hardware)

## Documentation Update Rule

- Update documentation frequently, not only at release time.
- For every code change that affects behavior, API, structure, setup, or examples, update the relevant docs in the same branch before merge to `dev`.
- Keep `README.md`, examples, and `AGENTS.md` aligned with the current implementation.

## Branching Best Practices

- Required flow: `main` -> `dev` -> `feature/*` or `fix/*` -> merge back to `dev` -> merge `dev` to `main`.
- Mandatory completion rule: when work is finished on any topic branch (`feature/*`, `fix/*`, `docs/*`, `chore/*`), it must be merged back into `dev`.
- Keep `dev` as the active integration branch for day-to-day development.
- Do not commit directly to `dev`; merge through pull requests.
- Keep `dev` releasable:
  - no knowingly broken tests
  - no incomplete hardware-critical behavior
  - no unresolved merge markers
- Rebase or merge from `dev` frequently to reduce long-lived drift in branch history.
- Require PR review for `dev` merges when possible.
- After tasks are finished and merged, local branches must be only:
  - `main`
  - `dev`
- Delete all merged topic branches (`feature/*`, `fix/*`, `docs/*`, `chore/*`) both:
  - locally
  - on remote (`origin`)

### `dev` Branch Rules

- Base all new work from the latest `dev`.
- Merge only focused branches (`feature/*` or `fix/*`) into `dev`.
- Prefer squash merge for noisy commit histories; preserve individual commits only when useful for audit/debug.
- Ensure PR description includes:
  - what changed
  - why it changed
  - how it was tested
  - hardware risk level (if servo behavior is affected)

### `feature/*` Branch Practices (Target: `dev`)

- Naming format: `feature/<short-kebab-description>`
  - Example: `feature/ax12-bulk-read`
- Scope to one feature or one coherent capability.
- Include tests and docs updates in the same branch when behavior changes.
- Open PR into `dev` early if implementation affects protocol, packet parsing, or motion safety.
- Avoid mixing unrelated refactors into feature branches.
- After merge into `dev`, delete the feature branch both:
  - locally
  - on remote (`origin`)

### `fix/*` Branch Practices (Target: `dev`)

- Naming format: `fix/<short-kebab-description>`
  - Example: `fix/checksum-validation-timeout`
- Keep fixes minimal and root-cause focused.
- Add regression tests or reproducible verification steps for each bug fix.
- Document impact clearly:
  - affected modules
  - user-visible behavior change
  - hardware safety implications
- Merge `fix/*` into `dev` quickly after validation to prevent duplicate bugs across branches.
- After merge into `dev`, delete the fix branch both:
  - locally
  - on remote (`origin`)

## Python Best Practices

- Target Python 3 code style and behavior.
- Keep each class in its own file (`one class per file`) unless there is a strong, documented reason to group them.
- Place all exception classes in an `exceptions/` package.
- Place all dataclasses in a `data/` package.
- Add docstrings everywhere:
  - every module
  - every class
  - every public function and method
  - non-trivial private helpers
- Use explicit imports and package-relative imports inside `pydynamixel`.
- Add type hints for public functions and class methods.
- Validate function inputs (IDs, register addresses, byte/word ranges).
- Raise clear exceptions with actionable messages.
- Every Python source file must begin with:
  - interpreter shebang (example: `#!/usr/bin/env python3`)
  - encoding declaration (example: `# -*- coding: utf-8 -*-`)
- Keep I/O boundaries clean:
  - Packet encoding/decoding stays in packet/transport layers.
  - Business logic stays in higher-level modules.
- Avoid duplicated constants; keep register and protocol constants centralized.
- Maintain backward compatibility where feasible; if breaking, document clearly.
- Prefer deterministic behavior:
  - configurable retries
  - explicit timeouts
  - predictable default values
- Add or update tests for bug fixes and new behavior.

## Dynamixel Servo Control Best Practices

- Use Protocol 1.0 behavior for AX-12/AX-12A.
- Treat all servo writes as potentially unsafe until validated.
- Always validate command ranges before sending:
  - ID: `0..253`
  - Position: `0..1023` (unless wheel mode configured)
  - Speed/Torque values: `0..1023`
- Use retries for communication noise, but fail fast on servo-reported fatal errors.
- Confirm packet checksum and expected response ID for every read/write transaction.
- Prefer `REG_WRITE` + `ACTION` for coordinated multi-servo moves.
- On startup, avoid jerk motion:
  - read present position
  - set goal position to current position
  - then command motion
- Keep torque safety in mind:
  - disable torque before changing critical configuration where appropriate
  - monitor load/temperature/voltage in long-running motion loops
- Respect thermal and voltage limits from control table defaults or configured values.
- Avoid unnecessary broadcast writes (`ID 254`); use only when intentional and safe.
- Implement safe-stop behavior in control loops:
  - timeout handling
  - exception path that stops motion commands
- Log enough telemetry for diagnosis:
  - servo ID
  - instruction/register
  - retries
  - returned error bits

## Review Checklist

- Change is minimal and focused.
- Public API remains coherent and documented.
- Error handling is explicit and tested.
- Hardware-facing code has bounds checks and safety guards.
- Examples/docs remain accurate after code changes.
