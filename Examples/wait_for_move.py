#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The following moves a servo to a target position and very slow velocity,
and waits for the servo to complete moving before turning on the LED and
printing a "Done moving!" message.

"""

from pydynamixel import dynamixel, registers
import time

def main():
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
        ser = dynamixel.get_serial_for_url(serial_port)

        dynamixel.set_led(ser, servo_id, registers.LED_STATE.OFF)

        if first_move:
            dynamixel.init(ser, servo_id)

        dynamixel.set_position(ser, servo_id, target_position)
        dynamixel.set_velocity(ser, servo_id, velocity)
        dynamixel.send_action_packet(ser)

        print("Waiting...")
        while dynamixel.get_is_moving(ser, servo_id):
            time.sleep(0.1)

        print("Done moving!")
        dynamixel.set_led(ser, servo_id, registers.LED_STATE.ON)
    except Exception as exc:
        print("ERROR!")
        print(exc)


if __name__ == "__main__":
    main()
