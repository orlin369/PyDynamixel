#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gripper-style torque-limited close loop using OO helpers."""

from pydynamixel import DynamixelBus, ServoChain

def grip(servo_chain, joint, incr, limit, velocity, verbose):
    """
    This function will modify the angular position of the servo with the specified ID until
    its measured torque exceeds a specified value. This is especailly useful for gripping objects, 
    as it allows objects of all sizes to be gripped.
    
    :param joint: The servo ID of the joint to manipulate.
    :param incr: The amount by which to increment (or decrement) the current angular position.
    :param limit: The torque limit, in Dynamixel units. 
    :param velocity: The velocity at which to change the position.
    :param verbose: If True, status information will be printed. Default: ``VERBOSE``.
    :param num_error_attempts: The number of attempts to make to send the packet when an error is encountered.
    
    :param servo_chain: ServoChain instance.
    :returns: The angular position at which the torque was exceeded.
    """
    bus = servo_chain.bus

    # The initial angular position
    val = servo_chain.read_position([joint])[0]

    # Loop forever
    while True:
        # Get the torque
        torque = bus.get_torque(joint)
        
        if verbose:
            print('Torque: {0}'.format(torque))

        # Check the torque. If greater than the limit, return.
        if torque >= limit:
            if verbose:
                print('Torque at limit!')
                
            return val
        
        # Otherwise, increment the angular position. 
        val += incr
        if verbose:
            print('Setting val to {0}.'.format(val))
        
        vector = servo_chain.make_vector_constant_velocity([val], [joint], velocity)
        servo_chain.move_to_vector(vector)
        servo_chain.wait_for_move([joint])
    
def main():
    """Continuously close grip until load threshold is reached."""
    url = '/dev/tty.usbserial-A9SFBTPX'
    bus = DynamixelBus.from_url(url, verbose=False, attempts=10)
    servo_chain = ServoChain(bus)
    
    verbose = False
    joint = 7
    limit = 700
    velocity = 100
    incr = 1
    
    grip(servo_chain, joint, incr, limit, velocity, verbose)


if __name__ == '__main__':
    main()
    
