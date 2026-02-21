#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example simply moves a specified servo to a specified position. 

Usage:
    python Examples/motion_test.py --port COM5 --id 1 --position 768 --init
    python Examples/motion_test.py --port /dev/ttyUSB0 --id 2 --position 512
"""

import argparse

from pydynamixel import DynamixelBus


def parse_args():
    """Parse command-line arguments for the single-servo motion example."""
    parser = argparse.ArgumentParser(description="Move one Dynamixel servo to a target position.")
    parser.add_argument("--port", required=True, help="Serial port path (example: COM5 or /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=1_000_000, help="Bus baudrate (default: 1000000).")
    parser.add_argument("--timeout", type=float, default=0.1, help="Read timeout in seconds (default: 0.1).")
    parser.add_argument("--id", type=int, default=9, help="Servo ID (default: 9).")
    parser.add_argument("--position", type=int, default=768, help="Target position (default: 768).")
    parser.add_argument("--init", action="store_true", help="Initialize servo to current position before moving.")
    return parser.parse_args()


def main():
    """Move one servo to a target position using the object-oriented bus API."""
    args = parse_args()
    try:
        bus = DynamixelBus.from_url(args.port, baudrate=args.baudrate, timeout=args.timeout, verbose=False, attempts=3)

        if args.init:
            bus.init_servo(args.id)

        bus.set_position(args.id, args.position)
        bus.send_action()

        print("Success!")
    except Exception as exc:
        print("Unable to move to desired position.")
        print(exc)


if __name__ == "__main__":
    main()
