#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The following moves a servo to a target position and very slow velocity,
and waits for the servo to complete moving before turning on the LED and
printing a "Done moving!" message.

"""

from pydynamixel import DynamixelBus, registers
import time

def main():
    """Move a servo and block until movement completes using OO helpers."""
    # You'll need to change this to the serial port of your USB2Dynamixel
    serial_port = "/dev/tty.usbserial-A921X77J"

    # You'll need to modify this for your setup
    servo_id = 9

    target_position = 0
    velocity = 20  # very slow

    # If this is the first time the robot was powered on, we need to read
    # and set the current position.
    first_move = True

    try:
        bus = DynamixelBus.from_url(serial_port)

        bus.set_led(servo_id, registers.LED_STATE.OFF)

        if first_move:
            bus.init_servo(servo_id)

        bus.set_position(servo_id, target_position)
        bus.set_velocity(servo_id, velocity)
        bus.send_action()

        print("Waiting...")
        while bus.get_is_moving(servo_id):
            time.sleep(0.1)

        print("Done moving!")
        bus.set_led(servo_id, registers.LED_STATE.ON)
    except Exception as exc:
        print("ERROR!")
        print(exc)


if __name__ == "__main__":
    main()
