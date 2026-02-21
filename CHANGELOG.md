# Changelog

All notable changes to this project are documented in this file.

## [1.1.0] - 2026-02-21

### Added
- Full AX-12/AX-12A Protocol 1.0 serial implementation without DLL dependencies.
- New object-oriented APIs:
  - `DynamixelBus` for bus-level communication.
  - `ServoChain` for coordinated multi-servo motion.
  - `AX12` register-access object model.
- New package structure for maintainability:
  - `pydynamixel/exceptions/` for exception types.
  - `pydynamixel/data/` for dataclasses.
- Project governance rules in `AGENTS.md` (branching flow, coding standards, docs cadence).

### Changed
- Examples migrated to Python 3 compatible behavior and updated APIs.
- `pydynamixel.chain` now delegates to OO services while preserving functional compatibility.
- Register/packet handling and control-table constants cleaned up for AX-12 accuracy.
- Shebang + UTF-8 encoding headers standardized across Python files.

### Fixed
- Multiple legacy Python 2 and API mismatches in examples.
- Packaging long description source now aligned with existing `README.md`.

## [1.0.0] - 2014-03-07

### Added
- Initial `pydynamixel` package structure (`dynamixel.py`, `chain.py`).
- Serial packet communication helpers and register-level access.
- Early examples and documentation.

### Changed
- Iterative fixes and docs updates through 2014 for motion/control helpers.
