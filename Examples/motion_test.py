#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This example simply moves a specified servo to a specified position. 
"""

from pydynamixel import DynamixelBus

def main():
    """Move one servo to a target position using the object-oriented bus API."""
    # You'll need to change this to the serial port of your USB2Dynamixel
    serial_port = "/dev/tty.usbserial-A921X77J"

    # You'll need to modify these for your setup
    servo_id = 9
    target_position = 768  # range: 0 to 1023

    # If this is the first time the robot was powered on,
    # you'll need to read and set the current position.
    first_move = True

    try:
        bus = DynamixelBus.from_url(serial_port)

        if first_move:
            bus.init_servo(servo_id)

        bus.set_position(servo_id, target_position)
        bus.send_action()

        print("Success!")
    except Exception as exc:
        print("Unable to move to desired position.")
        print(exc)


if __name__ == "__main__":
    main()
