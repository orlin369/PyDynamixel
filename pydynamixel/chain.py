#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Helpers for coordinated motion of multiple AX-12 servos."""

import time

from . import dynamixel

NUM_ERROR_ATTEMPTS = 10
SLEEP_TIME = 0.1
VERBOSE = True


def wait_for_move(ser, joints, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    for joint in joints:
        while True:
            moving = dynamixel.get_is_moving(ser, joint, verbose, num_error_attempts)
            if not moving:
                break
            time.sleep(SLEEP_TIME)


def move_to_vector(ser, vector, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    for servo_id, angle, velocity in vector:
        if verbose:
            print(f"Setting angle for {servo_id} to {angle}...")
        dynamixel.set_position(ser, servo_id, angle, verbose, num_error_attempts)

        if verbose:
            print(f"Setting velocity for {servo_id} to {velocity}...")
        dynamixel.set_velocity(ser, servo_id, velocity, verbose, num_error_attempts)

    if verbose:
        print("Sending action packet.")
    dynamixel.send_action_packet(ser)


def read_position(ser, joints, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    positions = []
    for joint in joints:
        if verbose:
            print(f"Reading initial position for joint {joint}...")
        positions.append(dynamixel.get_position(ser, joint, verbose, num_error_attempts))
    return positions


def make_vector_constant_velocity(position, joints, velocity):
    return [(joints[i], position[i], velocity) for i in range(len(joints))]


def make_vector(position, joints, velocity):
    return [(joints[i], position[i], velocity[i]) for i in range(len(joints))]


def init_constant_velocity(ser, joints, velocity, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    init_pos = read_position(ser, joints, verbose, num_error_attempts)
    vector = make_vector_constant_velocity(init_pos, joints, velocity)
    move_to_vector(ser, vector, verbose, num_error_attempts)
    wait_for_move(ser, joints, verbose, num_error_attempts)
    return vector


def init(ser, joints, velocity, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    init_pos = read_position(ser, joints, verbose, num_error_attempts)
    vector = make_vector(init_pos, joints, velocity)
    move_to_vector(ser, vector, verbose, num_error_attempts)
    wait_for_move(ser, joints, verbose, num_error_attempts)
    return vector

