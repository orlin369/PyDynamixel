#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The following code can be used to turn on the LED on a connected servo 
(on a POSIX-compliant platform.)

Usage:
    python Examples/led_test.py --port COM5 --id 1 --led on
    python Examples/led_test.py --port /dev/ttyUSB0 --id 1 --led off
"""

import argparse

from pydynamixel import DynamixelBus, registers


def parse_args():
    """Parse command-line arguments for LED example configuration."""
    parser = argparse.ArgumentParser(description="Set LED state on one Dynamixel servo.")
    parser.add_argument("--port", required=True, help="Serial port path (example: COM5 or /dev/ttyUSB0).")
    parser.add_argument("--baudrate", type=int, default=1_000_000, help="Bus baudrate (default: 1000000).")
    parser.add_argument("--timeout", type=float, default=0.1, help="Read timeout in seconds (default: 0.1).")
    parser.add_argument("--id", type=int, default=9, help="Servo ID (default: 9).")
    parser.add_argument("--led", choices=["on", "off"], default="on", help="LED state (default: on).")
    return parser.parse_args()


def main():
    """Turn one servo LED on or off using the object-oriented bus API."""
    args = parse_args()
    led_value = registers.LED_STATE.ON if args.led == "on" else registers.LED_STATE.OFF
    try:
        bus = DynamixelBus.from_url(args.port, baudrate=args.baudrate, timeout=args.timeout, verbose=False, attempts=3)
        bus.set_led(args.id, led_value)
        print("LED set successfully!")
    except Exception as exc:
        print("Unable to set LED.")
        print(exc)


if __name__ == "__main__":
    main()
