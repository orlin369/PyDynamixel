#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Interactive position monitor using the object-oriented chain helper."""

from pydynamixel import DynamixelBus, ServoChain

def display_position(servo_chain, joints):
    """
    This example will display the current position of the specified axes whenever the
    the ``ENTER`` key is pressed. 
    
    :param servo_chain: ServoChain instance.
    :param joints: A list of servo IDs. 
    
    :returns: ``None``
    """
    prompt = "Press <ENTER> to display current position. Use q<ENTER> to quit: "
    
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "q":
            break
        
        vector = servo_chain.read_position(joints)
        print(vector)
        
def main():
    """Run interactive joint position display."""
    url = '/dev/tty.usbserial-A9SFBTPX'
    bus = DynamixelBus.from_url(url, verbose=False, attempts=10)
    servo_chain = ServoChain(bus)

    joints = [1, 2, 3, 4, 5, 6, 7]
    
    display_position(servo_chain, joints)


if __name__ == '__main__':
    main()
    
