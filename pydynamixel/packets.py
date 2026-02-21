"""Packet utilities for Dynamixel Protocol 1.0 (AX-12 family)."""

from . import registers


def checksum(data_bytes):
    """Return protocol-1 checksum for bytes starting at ID field."""
    return (~(sum(data_bytes) & 0xFF)) & 0xFF


def get_packet(payload):
    """Return a full packet as bytes from payload [ID, LENGTH, INSTR, ...params]."""
    data = list(payload)
    return bytes([0xFF, 0xFF] + data + [checksum(data)])


def instruction_packet(servo_id, instruction, params=()):
    """Build a generic instruction packet."""
    params = list(params)
    length = len(params) + 2
    return get_packet([servo_id & 0xFF, length, instruction & 0xFF] + params)


def get_ping_packet(servo_id):
    return instruction_packet(servo_id, registers.INSTRUCTION.PING)


def get_action_packet():
    return instruction_packet(registers.BROADCAST_ID, registers.INSTRUCTION.ACTION)


def get_reset_packet(servo_id):
    return instruction_packet(servo_id, registers.INSTRUCTION.RESET)


def get_write_packet_1b(servo_id, register, data):
    return instruction_packet(
        servo_id,
        registers.INSTRUCTION.WRITE_DATA,
        [register & 0xFF, data & 0xFF],
    )


def get_write_packet_2b(servo_id, register, data):
    lsb = data & 0xFF
    msb = (data >> 8) & 0xFF
    return instruction_packet(
        servo_id,
        registers.INSTRUCTION.WRITE_DATA,
        [register & 0xFF, lsb, msb],
    )


def get_reg_write_packet_1b(servo_id, register, data):
    return instruction_packet(
        servo_id,
        registers.INSTRUCTION.REG_WRITE,
        [register & 0xFF, data & 0xFF],
    )


def get_reg_write_packet_2b(servo_id, register, data):
    lsb = data & 0xFF
    msb = (data >> 8) & 0xFF
    return instruction_packet(
        servo_id,
        registers.INSTRUCTION.REG_WRITE,
        [register & 0xFF, lsb, msb],
    )


def get_read_packet(servo_id, register, num_bytes=2):
    return instruction_packet(
        servo_id,
        registers.INSTRUCTION.READ_DATA,
        [register & 0xFF, num_bytes & 0xFF],
    )


def get_write_position_packet(servo_id, position):
    return get_write_packet_2b(servo_id, registers.GOAL_POSITION, position)


def get_write_velocity_packet(servo_id, velocity):
    return get_write_packet_2b(servo_id, registers.MOVING_SPEED, velocity)


def get_write_led_packet(servo_id, value):
    return get_write_packet_1b(servo_id, registers.LED, value)


def get_read_position_packet(servo_id):
    return get_read_packet(servo_id, registers.PRESENT_POSITION, 2)


def get_read_torque_packet(servo_id):
    return get_read_packet(servo_id, registers.PRESENT_LOAD, 2)


def get_read_is_moving_packet(servo_id):
    return get_read_packet(servo_id, registers.MOVING, 1)
