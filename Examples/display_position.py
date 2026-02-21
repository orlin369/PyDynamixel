#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Interactive position monitor using the object-oriented chain helper.

Usage:
    python Examples/display_position.py --port COM5 --joints 1,2,3
    python Examples/display_position.py --port /dev/ttyUSB0 --joints 1,2,3,4,5,6
"""

import argparse

from pydynamixel import DynamixelBus, ServoChain


def parse_args():
    """Parse command-line arguments for the interactive position monitor."""
    parser = argparse.ArgumentParser(description="Display current positions for a list of servo IDs.")
    parser.add_argument("--port", required=True, help="Serial port path (example: COM5 or /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=1_000_000, help="Bus baudrate (default: 1000000).")
    parser.add_argument("--timeout", type=float, default=0.1, help="Read timeout in seconds (default: 0.1).")
    parser.add_argument(
        "--joints",
        default="1,2,3,4,5,6,7",
        help="Comma-separated servo IDs to monitor (default: 1,2,3,4,5,6,7).",
    )
    return parser.parse_args()


def display_position(servo_chain, joints):
    """Print joint positions each time ENTER is pressed."""
    prompt = "Press <ENTER> to display current position. Use q<ENTER> to quit: "

    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "q":
            break

        vector = servo_chain.read_position(joints)
        print(vector)


def main():
    """Run interactive joint position display."""
    args = parse_args()
    joints = [int(item.strip()) for item in args.joints.split(",") if item.strip()]
    bus = DynamixelBus.from_url(args.port, baudrate=args.baudrate, timeout=args.timeout, verbose=False, attempts=3)
    servo_chain = ServoChain(bus)
    display_position(servo_chain, joints)


if __name__ == "__main__":
    main()
