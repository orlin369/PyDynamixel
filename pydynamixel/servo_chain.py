#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Object-oriented helpers for synchronized multi-servo motion."""

import time
from typing import List, Sequence, Tuple

from .dynamixel_bus import DynamixelBus

Vector = List[Tuple[int, int, int]]


class ServoChain:
    """Coordinate multi-servo motions over a shared bus."""

    def __init__(self, bus: DynamixelBus, sleep_time: float = 0.1):
        """Initialize chain helper.

        Args:
            bus: DynamixelBus instance used for communication.
            sleep_time: Poll interval while waiting for movement completion.
        """
        self.bus = bus
        self.sleep_time = sleep_time

    def wait_for_move(self, joints: Sequence[int]) -> None:
        """Block until all listed joints stop moving."""
        for joint in joints:
            while self.bus.get_is_moving(joint):
                time.sleep(self.sleep_time)

    def move_to_vector(self, vector: Sequence[Tuple[int, int, int]]) -> None:
        """Stage position/speed writes for all joints and execute one action."""
        for servo_id, angle, velocity in vector:
            self.bus.set_position(servo_id, angle)
            self.bus.set_velocity(servo_id, velocity)
        self.bus.send_action()

    def read_position(self, joints: Sequence[int]) -> List[int]:
        """Read current positions for all joints in order."""
        return [self.bus.get_position(joint) for joint in joints]

    @staticmethod
    def make_vector_constant_velocity(position: Sequence[int], joints: Sequence[int], velocity: int) -> Vector:
        """Build vector tuples from positions and one shared velocity."""
        return [(joints[i], position[i], velocity) for i in range(len(joints))]

    @staticmethod
    def make_vector(position: Sequence[int], joints: Sequence[int], velocity: Sequence[int]) -> Vector:
        """Build vector tuples from positions and per-joint velocities."""
        return [(joints[i], position[i], velocity[i]) for i in range(len(joints))]

    def init_constant_velocity(self, joints: Sequence[int], velocity: int) -> Vector:
        """Initialize joints by commanding current positions at one velocity."""
        init_pos = self.read_position(joints)
        vector = self.make_vector_constant_velocity(init_pos, joints, velocity)
        self.move_to_vector(vector)
        self.wait_for_move(joints)
        return vector

    def init(self, joints: Sequence[int], velocity: Sequence[int]) -> Vector:
        """Initialize joints by commanding current positions at per-joint velocities."""
        init_pos = self.read_position(joints)
        vector = self.make_vector(init_pos, joints, velocity)
        self.move_to_vector(vector)
        self.wait_for_move(joints)
        return vector
