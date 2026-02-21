#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydynamixel import chain, dynamixel

def display_position(ser, joints, verbose=False, num_error_attempts=10):
    """
    This example will display the current position of the specified axes whenever the
    the ``ENTER`` key is pressed. 
    
    :param ser: The ``serial`` port to use. 
    :param joints: A list of servo IDs. 
    :param verbose: If True, status information will be printed. Default: ``VERBOSE``.
    :param num_error_attempts: The number of attempts to make to send the packet when an error is encountered.
    
    :returns: ``None``
    """
    
    # Clear any data in the serial buffer
    dynamixel.flush_serial(ser)
    
    prompt = "Press <ENTER> to display current position. Use q<ENTER> to quit: "
    
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "q":
            break
        
        vector = chain.read_position(ser, joints, verbose, num_error_attempts)
        print(vector)
        
if __name__ == '__main__':
    url = '/dev/tty.usbserial-A9SFBTPX'
    ser = dynamixel.get_serial_for_url(url)
    
    verbose = False
    joints = [1, 2, 3, 4, 5, 6, 7]
    num_error_attempts = 10
    
    display_position(ser, joints, verbose, num_error_attempts)
    
