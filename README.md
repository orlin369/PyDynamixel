# PyDynamixel

`PyDynamixel` is a Python library for controlling Dynamixel AX-12/AX-12A servos
using Dynamixel Protocol 1.0 over `pyserial` (no DLL required).

## Requirements

- Python `>=3.9`
- `pyserial>=3.5`
- Dynamixel Protocol 1.0 compatible hardware (AX-12/AX-12A tested)

## Features

- Pure Python serial communication.
- Object-oriented API:
  - `DynamixelBus` for bus-level operations.
  - `ServoChain` for synchronized multi-servo control.
  - `AX12` for per-servo register access.
- Backward-compatible functional wrappers in `pydynamixel.dynamixel` and `pydynamixel.chain`.
- Safety-oriented retry handling and register range validation.

## Installation

```bash
pip install .
```

### Install In `.venv` From GitHub (orlin369)

```bash
python -m venv .venv
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install directly from your GitHub repository:

```bash
pip install "git+https://github.com/orlin369/PyDynamixel.git@main"
```

Or install from `dev` branch:

```bash
pip install "git+https://github.com/orlin369/PyDynamixel.git@dev"
```

Or build/install as a package:

```bash
pip install build
python -m build
pip install dist/*.whl
```

## Quick Start (Object-Oriented API)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydynamixel import DynamixelBus, ServoChain, registers

bus = DynamixelBus.from_url("/dev/tty.usbserial-A921X77J", verbose=False, attempts=10)
chain = ServoChain(bus)

servo_id = 1
bus.set_led(servo_id, registers.LED_STATE.ON)
bus.init_servo(servo_id)
bus.set_position(servo_id, 512)
bus.set_velocity(servo_id, 120)
bus.send_action()
```

## Quick Start (Functional Compatibility API)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydynamixel import dynamixel, registers

ser = dynamixel.get_serial_for_url("/dev/tty.usbserial-A921X77J")
servo_id = 1

dynamixel.set_led(ser, servo_id, registers.LED_STATE.ON)
dynamixel.init(ser, servo_id)
dynamixel.set_position(ser, servo_id, 512)
dynamixel.set_velocity(ser, servo_id, 120)
dynamixel.send_action_packet(ser)
```

## Functional Compatibility API

Legacy code can still use:

- `pydynamixel.dynamixel`
- `pydynamixel.chain`

## Included Examples

See `Examples/`:

- `led_test.py`
- `motion_test.py`
- `wait_for_move.py`
- `display_position.py`
- `grip.py`

## Development Workflow

- Active integration branch: `dev`
- Release branch: `main`
- Work branches: `feature/*`, `fix/*`, `docs/*`, `chore/*`
- Merge flow: topic branch -> `dev` -> `main`
- Pull requests are not required for this repository workflow.

## Development Notes

- Project version: `1.2.0`
- Change history: `CHANGELOG.md`
- Contribution and workflow rules: `AGENTS.md`
- Maintainer: `orlin369`
