#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Pure-pyserial AX-12/AX-12A implementation (Dynamixel Protocol 1.0)."""

from typing import Iterable

import serial

from . import packets, registers
from .ax12 import AX12
from .dynamixel_fatal_error import DynamixelFatalError
from .response import Response

# The number of retries used for noisy half-duplex buses.
NUM_ERROR_ATTEMPTS = 10
VERBOSE = True

# Backwards-compatible aliases.
BROADCAST = registers.BROADCAST_ID
BAUDRATE = registers.DEFAULT_BAUDRATE
TIMEOUT = registers.DEFAULT_TIMEOUT


def get_serial_for_url(url, baudrate=BAUDRATE, timeout=TIMEOUT):
    ser = serial.serial_for_url(url)
    ser.baudrate = baudrate
    ser.timeout = timeout
    return ser


def get_serial_for_com(com, baudrate=BAUDRATE, timeout=TIMEOUT):
    ser = serial.Serial(com)
    ser.baudrate = baudrate
    ser.timeout = timeout
    return ser


def flush_serial(ser):
    """Clear both serial buffers."""
    if hasattr(ser, "reset_input_buffer"):
        ser.reset_input_buffer()
    else:
        while ser.inWaiting() > 0:
            ser.read(1)
    if hasattr(ser, "reset_output_buffer"):
        ser.reset_output_buffer()


def get_error_string(error):
    errors = []
    if error & registers.ERROR_BIT_MASKS.INPUT_VOLTAGE:
        errors.append("input voltage error")
    if error & registers.ERROR_BIT_MASKS.ANGLE_LIMIT:
        errors.append("angle limit error")
    if error & registers.ERROR_BIT_MASKS.OVERHEATING:
        errors.append("motor overheating")
    if error & registers.ERROR_BIT_MASKS.RANGE:
        errors.append("range error")
    if error & registers.ERROR_BIT_MASKS.SEND_CHECKSUM:
        errors.append("checksum mismatch")
    if error & registers.ERROR_BIT_MASKS.OVERLOAD:
        errors.append("motor overloaded")
    if error & registers.ERROR_BIT_MASKS.INSTRUCTION:
        errors.append("instruction error")

    if not errors:
        return None
    if len(errors) == 1:
        return errors[0].capitalize()
    return ", ".join(s.capitalize() for s in errors[:-1]) + " and " + errors[-1].capitalize()


def get_exception(error_code):
    if error_code == registers.ERROR_BIT_MASKS.SEND_CHECKSUM:
        return Exception("Send checksum mismatch.")
    return DynamixelFatalError(get_error_string(error_code) or "Unknown Dynamixel error.")


def _read_exact(ser, size):
    data = ser.read(size)
    if data is None or len(data) != size:
        raise TimeoutError(f"Serial timeout while reading {size} bytes (got {0 if data is None else len(data)}).")
    return data


def get_response(ser):
    """Read and decode one status packet."""
    last = None
    while True:
        b = _read_exact(ser, 1)[0]
        if b == 0xFF and last == 0xFF:
            break
        last = b

    servo_id = _read_exact(ser, 1)[0]
    length = _read_exact(ser, 1)[0]
    error = _read_exact(ser, 1)[0]

    param_len = length - 2
    params = list(_read_exact(ser, param_len)) if param_len > 0 else []
    checksum = _read_exact(ser, 1)[0]

    calc = packets.checksum([servo_id, length, error] + params)
    if checksum != calc:
        raise Exception(f"Checksum mismatch ({checksum} vs {calc}).")

    return Response(servo_id, error, params, True)


def write_and_get_response_multiple(
    ser,
    packet,
    servo_id=None,
    verbose=VERBOSE,
    attempts=NUM_ERROR_ATTEMPTS,
):
    """Write packet and retry until a valid response is received."""
    if isinstance(packet, list):
        packet = bytes(packet)

    for i in range(attempts):
        try:
            flush_serial(ser)
            ser.write(packet)
            response = get_response(ser)

            if servo_id is not None and response.servo_id != servo_id:
                raise Exception(f"Got packet from {response.servo_id}, expected {servo_id}.")
            if not response.checksum_match:
                raise Exception("Checksum mismatch.")
            if response.error > 0:
                raise get_exception(response.error)
            return response
        except DynamixelFatalError:
            raise
        except Exception as exc:
            if verbose:
                print(f"Got exception when waiting for response from {servo_id} on attempt {i + 1}: {exc}")

    raise Exception(f"Unable to read response for servo {servo_id}")


def _require_range(name, value, minimum, maximum):
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be in range [{minimum}, {maximum}], got {value}.")


def ping(ser, servo_id, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    packet = packets.get_ping_packet(servo_id)
    try:
        write_and_get_response_multiple(ser, packet, servo_id, verbose, num_error_attempts)
        return True
    except Exception:
        return False


def scan(ser, begin_id=0, end_id=253, verbose=False):
    found = []
    for sid in range(begin_id, end_id + 1):
        if ping(ser, sid, verbose=verbose, num_error_attempts=1):
            found.append(sid)
    return found


def get_read_packet(servo_id, register, num_bytes=2):
    return packets.get_read_packet(servo_id, register, num_bytes)


def read_data(ser, servo_id, register, num_bytes, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    packet = packets.get_read_packet(servo_id, register, num_bytes)
    resp = write_and_get_response_multiple(ser, packet, servo_id, verbose, num_error_attempts)
    if len(resp.data) != num_bytes:
        raise Exception(f"Read length mismatch (expected {num_bytes}, got {len(resp.data)}).")
    return resp.data


def read_byte(ser, servo_id, register, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    return read_data(ser, servo_id, register, 1, verbose, num_error_attempts)[0]


def read_word(ser, servo_id, register, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    data = read_data(ser, servo_id, register, 2, verbose, num_error_attempts)
    return (data[1] << 8) | data[0]


def write_byte(ser, servo_id, register, value, deferred=False, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    _require_range("byte value", value, 0, 0xFF)
    if deferred:
        packet = packets.get_reg_write_packet_1b(servo_id, register, value)
    else:
        packet = packets.get_write_packet_1b(servo_id, register, value)
    write_and_get_response_multiple(ser, packet, servo_id, verbose, num_error_attempts)


def write_word(ser, servo_id, register, value, deferred=False, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    _require_range("word value", value, 0, 0xFFFF)
    if deferred:
        packet = packets.get_reg_write_packet_2b(servo_id, register, value)
    else:
        packet = packets.get_write_packet_2b(servo_id, register, value)
    write_and_get_response_multiple(ser, packet, servo_id, verbose, num_error_attempts)


def send_action_packet(ser):
    ser.write(packets.get_action_packet())


def set_led(ser, servo_id, value, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    write_byte(ser, servo_id, registers.LED, value, False, verbose, num_error_attempts)


def get_torque(ser, servo_id, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    return read_word(ser, servo_id, registers.PRESENT_LOAD, verbose, num_error_attempts)


def get_position(ser, servo_id, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    return read_word(ser, servo_id, registers.PRESENT_POSITION, verbose, num_error_attempts)


def set_position(ser, servo_id, position, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    _require_range("position", position, registers.POSITION_MIN, registers.POSITION_MAX)
    write_word(ser, servo_id, registers.GOAL_POSITION, position, True, verbose, num_error_attempts)


def set_velocity(ser, servo_id, velocity, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    _require_range("velocity", velocity, registers.SPEED_MIN, registers.SPEED_MAX)
    write_word(ser, servo_id, registers.MOVING_SPEED, velocity, True, verbose, num_error_attempts)


def set_torque_enable(ser, servo_id, enabled, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    write_byte(ser, servo_id, registers.TORQUE_ENABLE, 1 if enabled else 0, False, verbose, num_error_attempts)


def get_is_moving(ser, servo_id, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    return bool(read_byte(ser, servo_id, registers.MOVING, verbose, num_error_attempts))


def init(ser, servo_id, verbose=VERBOSE, num_error_attempts=NUM_ERROR_ATTEMPTS):
    position = get_position(ser, servo_id, verbose, num_error_attempts)
    set_position(ser, servo_id, position, verbose, num_error_attempts)
    send_action_packet(ser)


def get_ax12(ser, servo_id):
    return AX12(ser, servo_id)


def get_ax12_chain(ser, ids: Iterable[int]):
    return [AX12(ser, servo_id) for servo_id in ids]
