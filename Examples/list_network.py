#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Scan and list all reachable servos on a Dynamixel bus.

Usage:
    python Examples/list_network.py --port COM5
    python Examples/list_network.py --port /dev/ttyUSB0 --start-id 1 --end-id 20
"""

import argparse

from pydynamixel import DynamixelBus


def parse_args():
    """Parse command-line arguments for bus scan configuration."""
    parser = argparse.ArgumentParser(description="List all servos reachable on the Dynamixel network.")
    parser.add_argument("--port", required=True, help="Serial port path (example: COM5 or /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=1_000_000, help="Bus baudrate (default: 1000000).")
    parser.add_argument("--timeout", type=float, default=0.1, help="Read timeout in seconds (default: 0.1).")
    parser.add_argument("--start-id", type=int, default=0, help="First ID to probe (default: 0).")
    parser.add_argument("--end-id", type=int, default=253, help="Last ID to probe (default: 253).")
    return parser.parse_args()


def main():
    """Connect to the bus, scan IDs, and print discovered servo details."""
    args = parse_args()

    bus = DynamixelBus.from_url(
        args.port,
        baudrate=args.baudrate,
        timeout=args.timeout,
        verbose=False,
        attempts=3,
    )

    servo_ids = bus.scan(begin_id=args.start_id, end_id=args.end_id)

    if not servo_ids:
        print("No servos found.")
        return

    print(f"Found {len(servo_ids)} servo(s): {servo_ids}")
    print("ID | Model | FW | Voltage(0.1V) | Temp(C)")
    print("---+-------+----+---------------+--------")

    for servo_id in servo_ids:
        servo = bus.servo(servo_id)
        try:
            print(
                f"{servo_id:>2} | "
                f"{servo.model_number:>5} | "
                f"{servo.version:>2} | "
                f"{servo.present_voltage:>13} | "
                f"{servo.present_temperature:>6}"
            )
        except Exception as exc:
            # Continue listing remaining devices if one read fails.
            print(f"{servo_id:>2} | read error: {exc}")


if __name__ == "__main__":
    main()
