# PyDynamixel

`PyDynamixel` is a Python library for controlling Dynamixel AX-12/AX-12A servos
using Dynamixel Protocol 1.0 over `pyserial` (no DLL required).

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

Or build/install as a package:

```bash
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

## Development Notes

- Project version: `1.2.0`
- Change history: `CHANGELOG.md`
- Contribution and workflow rules: `AGENTS.md`
