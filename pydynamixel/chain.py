#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Backward-compatible functional wrappers for synchronized servo control."""

from .dynamixel_bus import DynamixelBus
from .servo_chain import ServoChain

NUM_ERROR_ATTEMPTS = 10
SLEEP_TIME = 0.1
VERBOSE = True


def _make_chain(ser, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    """Construct a ServoChain from legacy function-call arguments."""
    bus = DynamixelBus(ser, verbose=verbose, attempts=num_error_attempts)
    return ServoChain(bus, sleep_time=SLEEP_TIME)


def wait_for_move(ser, joints, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    """Wait until all joints stop moving."""
    _make_chain(ser, verbose, num_error_attempts).wait_for_move(joints)


def move_to_vector(ser, vector, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    """Move all joints described by vector tuples."""
    _make_chain(ser, verbose, num_error_attempts).move_to_vector(vector)


def read_position(ser, joints, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    """Read positions for listed joints."""
    return _make_chain(ser, verbose, num_error_attempts).read_position(joints)


def make_vector_constant_velocity(position, joints, velocity):
    """Build vector tuples from positions and one shared velocity."""
    return ServoChain.make_vector_constant_velocity(position, joints, velocity)


def make_vector(position, joints, velocity):
    """Build vector tuples from positions and per-joint velocities."""
    return ServoChain.make_vector(position, joints, velocity)


def init_constant_velocity(ser, joints, velocity, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    """Initialize joints to their current positions at one shared velocity."""
    return _make_chain(ser, verbose, num_error_attempts).init_constant_velocity(joints, velocity)


def init(ser, joints, velocity, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    """Initialize joints to their current positions at per-joint velocities."""
    return _make_chain(ser, verbose, num_error_attempts).init(joints, velocity)
