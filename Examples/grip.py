#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gripper-style torque-limited close loop using OO helpers.

Usage:
    python Examples/grip.py --port COM5 --id 7 --limit 700 --velocity 100 --incr 1 --verbose
    python Examples/grip.py --port /dev/ttyUSB0 --id 5 --limit 600 --velocity 80 --incr -1
"""

import argparse

from pydynamixel import DynamixelBus, ServoChain


def parse_args():
    """Parse command-line arguments for the torque-limited grip example."""
    parser = argparse.ArgumentParser(description="Close one servo until torque reaches a threshold.")
    parser.add_argument("--port", required=True, help="Serial port path (example: COM5 or /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=1_000_000, help="Bus baudrate (default: 1000000).")
    parser.add_argument("--timeout", type=float, default=0.1, help="Read timeout in seconds (default: 0.1).")
    parser.add_argument("--id", type=int, default=7, help="Servo ID (default: 7).")
    parser.add_argument("--incr", type=int, default=1, help="Position increment per step (default: 1).")
    parser.add_argument("--limit", type=int, default=700, help="Torque threshold (default: 700).")
    parser.add_argument("--velocity", type=int, default=100, help="Step velocity (default: 100).")
    parser.add_argument("--verbose", action="store_true", help="Enable step-by-step logging.")
    return parser.parse_args()


def grip(servo_chain, joint, incr, limit, velocity, verbose):
    """Increase/decrease joint position until load exceeds limit."""
    bus = servo_chain.bus
    val = servo_chain.read_position([joint])[0]

    while True:
        torque = bus.get_torque(joint)

        if verbose:
            print(f"Torque: {torque}")

        if torque >= limit:
            if verbose:
                print("Torque at limit!")
            return val

        val += incr
        if verbose:
            print(f"Setting val to {val}.")

        vector = servo_chain.make_vector_constant_velocity([val], [joint], velocity)
        servo_chain.move_to_vector(vector)
        servo_chain.wait_for_move([joint])


def main():
    """Continuously close grip until load threshold is reached."""
    args = parse_args()
    bus = DynamixelBus.from_url(args.port, baudrate=args.baudrate, timeout=args.timeout, verbose=False, attempts=3)
    servo_chain = ServoChain(bus)
    grip(servo_chain, args.id, args.incr, args.limit, args.velocity, args.verbose)


if __name__ == "__main__":
    main()
