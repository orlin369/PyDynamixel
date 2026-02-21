#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The following code can be used to turn on the LED on a connected servo 
(on a POSIX-compliant platform.)
"""

from pydynamixel import DynamixelBus, registers

def main():
    """Turn the servo LED on using the object-oriented bus API."""
    # You'll need to change this to the serial port of your USB2Dynamixel
    serial_port = "/dev/tty.usbserial-A921X77J"

    # You'll need to change this to the ID of your servo
    servo_id = 9

    # Turn the LED on
    led_value = registers.LED_STATE.ON

    try:
        bus = DynamixelBus.from_url(serial_port)
        bus.set_led(servo_id, led_value)
        print("LED set successfully!")
    except Exception as exc:
        print("Unable to set LED.")
        print(exc)


if __name__ == "__main__":
    main()
