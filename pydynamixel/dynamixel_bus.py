#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Object-oriented bus controller for Dynamixel Protocol 1.0."""

from typing import Iterable, List

from . import registers
from .ax12 import AX12
from . import dynamixel


class DynamixelBus:
    """High-level object wrapper around a configured serial Dynamixel bus."""

    def __init__(self, serial_port, verbose: bool = True, attempts: int = 10):
        """Initialize a bus wrapper.

        Args:
            serial_port: Open pyserial-compatible port object.
            verbose: Print retry diagnostics when communication fails.
            attempts: Number of retries for request/response exchanges.
        """
        self.serial = serial_port
        self.verbose = verbose
        self.attempts = attempts

    @classmethod
    def from_url(cls, url: str, baudrate: int = registers.DEFAULT_BAUDRATE, timeout: float = registers.DEFAULT_TIMEOUT, verbose: bool = True, attempts: int = 10):
        """Create a bus from a serial URL path."""
        serial_port = dynamixel.get_serial_for_url(url, baudrate=baudrate, timeout=timeout)
        return cls(serial_port, verbose=verbose, attempts=attempts)

    @classmethod
    def from_com(cls, com: str, baudrate: int = registers.DEFAULT_BAUDRATE, timeout: float = registers.DEFAULT_TIMEOUT, verbose: bool = True, attempts: int = 10):
        """Create a bus from a COM device path."""
        serial_port = dynamixel.get_serial_for_com(com, baudrate=baudrate, timeout=timeout)
        return cls(serial_port, verbose=verbose, attempts=attempts)

    def flush(self) -> None:
        """Flush serial buffers."""
        dynamixel.flush_serial(self.serial)

    def ping(self, servo_id: int) -> bool:
        """Ping a single servo ID."""
        return dynamixel.ping(self.serial, servo_id, verbose=self.verbose, num_error_attempts=self.attempts)

    def scan(self, begin_id: int = 0, end_id: int = 253) -> List[int]:
        """Scan a range of IDs and return responsive IDs."""
        return dynamixel.scan(self.serial, begin_id=begin_id, end_id=end_id, verbose=self.verbose)

    def read_byte(self, servo_id: int, register: int) -> int:
        """Read one byte from a servo register."""
        return dynamixel.read_byte(self.serial, servo_id, register, verbose=self.verbose, num_error_attempts=self.attempts)

    def read_word(self, servo_id: int, register: int) -> int:
        """Read one word from a servo register."""
        return dynamixel.read_word(self.serial, servo_id, register, verbose=self.verbose, num_error_attempts=self.attempts)

    def write_byte(self, servo_id: int, register: int, value: int, deferred: bool = False) -> None:
        """Write one byte to a servo register."""
        dynamixel.write_byte(
            self.serial,
            servo_id,
            register,
            value,
            deferred=deferred,
            verbose=self.verbose,
            num_error_attempts=self.attempts,
        )

    def write_word(self, servo_id: int, register: int, value: int, deferred: bool = False) -> None:
        """Write one word to a servo register."""
        dynamixel.write_word(
            self.serial,
            servo_id,
            register,
            value,
            deferred=deferred,
            verbose=self.verbose,
            num_error_attempts=self.attempts,
        )

    def send_action(self) -> None:
        """Send ACTION broadcast packet."""
        dynamixel.send_action_packet(self.serial)

    def set_led(self, servo_id: int, value: int) -> None:
        """Set LED register."""
        dynamixel.set_led(self.serial, servo_id, value, verbose=self.verbose, num_error_attempts=self.attempts)

    def get_position(self, servo_id: int) -> int:
        """Read present position."""
        return dynamixel.get_position(self.serial, servo_id, verbose=self.verbose, num_error_attempts=self.attempts)

    def set_position(self, servo_id: int, position: int) -> None:
        """Set goal position using deferred write."""
        dynamixel.set_position(self.serial, servo_id, position, verbose=self.verbose, num_error_attempts=self.attempts)

    def set_velocity(self, servo_id: int, velocity: int) -> None:
        """Set moving speed using deferred write."""
        dynamixel.set_velocity(self.serial, servo_id, velocity, verbose=self.verbose, num_error_attempts=self.attempts)

    def get_is_moving(self, servo_id: int) -> bool:
        """Read moving flag."""
        return dynamixel.get_is_moving(self.serial, servo_id, verbose=self.verbose, num_error_attempts=self.attempts)

    def get_torque(self, servo_id: int) -> int:
        """Read present load/torque value."""
        return dynamixel.get_torque(self.serial, servo_id, verbose=self.verbose, num_error_attempts=self.attempts)

    def init_servo(self, servo_id: int) -> None:
        """Initialize a servo to current position to avoid startup jerk."""
        dynamixel.init(self.serial, servo_id, verbose=self.verbose, num_error_attempts=self.attempts)

    def servo(self, servo_id: int) -> AX12:
        """Create an AX12 object bound to this bus."""
        return AX12(self.serial, servo_id)

    def servos(self, ids: Iterable[int]) -> List[AX12]:
        """Create AX12 objects for a list of IDs."""
        return [AX12(self.serial, servo_id) for servo_id in ids]
