#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Move one servo and wait until movement is complete.

Usage:
    python Examples/wait_for_move.py --port COM5 --id 1 --position 0 --velocity 20 --init
    python Examples/wait_for_move.py --port /dev/ttyUSB0 --id 2 --position 800 --velocity 100
"""

import argparse
import time

from pydynamixel import DynamixelBus, registers


def parse_args():
    """Parse command-line arguments for wait-for-move example configuration."""
    parser = argparse.ArgumentParser(description="Move one servo and wait until it stops moving.")
    parser.add_argument("--port", required=True, help="Serial port path (example: COM5 or /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=1_000_000, help="Bus baudrate (default: 1000000).")
    parser.add_argument("--timeout", type=float, default=0.1, help="Read timeout in seconds (default: 0.1).")
    parser.add_argument("--id", type=int, default=9, help="Servo ID (default: 9).")
    parser.add_argument("--position", type=int, default=0, help="Target position (default: 0).")
    parser.add_argument("--velocity", type=int, default=20, help="Target velocity (default: 20).")
    parser.add_argument("--init", action="store_true", help="Initialize servo to current position before moving.")
    return parser.parse_args()


def main():
    """Move a servo and block until movement completes using OO helpers."""
    args = parse_args()

    try:
        bus = DynamixelBus.from_url(args.port, baudrate=args.baudrate, timeout=args.timeout, verbose=False, attempts=3)

        bus.set_led(args.id, registers.LED_STATE.OFF)

        if args.init:
            bus.init_servo(args.id)

        bus.set_position(args.id, args.position)
        bus.set_velocity(args.id, args.velocity)
        bus.send_action()

        print("Waiting...")
        while bus.get_is_moving(args.id):
            time.sleep(0.1)

        print("Done moving!")
        bus.set_led(args.id, registers.LED_STATE.ON)
    except Exception as exc:
        print("ERROR!")
        print(exc)


if __name__ == "__main__":
    main()
