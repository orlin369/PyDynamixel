#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AX-12 object-oriented register access."""

from . import registers


class AX12:
    """Object-oriented AX-12 register access over serial."""

    def __init__(self, ser, servo_id):
        self.ser = ser
        self.servo_id = servo_id

    def _backend(self):
        # Local import avoids import cycles with pydynamixel.dynamixel.
        from . import dynamixel

        return dynamixel

    def _rb(self, addr):
        return self._backend().read_byte(self.ser, self.servo_id, addr)

    def _rw(self, addr):
        return self._backend().read_word(self.ser, self.servo_id, addr)

    def _wb(self, addr, value):
        self._backend().write_byte(self.ser, self.servo_id, addr, value)

    def _ww(self, addr, value):
        self._backend().write_word(self.ser, self.servo_id, addr, value)

    @property
    def model_number(self):
        return self._rw(registers.MODEL_NUMBER)

    @property
    def version(self):
        return self._rb(registers.VERSION)

    @property
    def id(self):
        return self._rb(registers.ID)

    @id.setter
    def id(self, value):
        self._wb(registers.ID, value)
        self.servo_id = value

    @property
    def baud_rate(self):
        return self._rb(registers.BAUD_RATE)

    @baud_rate.setter
    def baud_rate(self, value):
        self._wb(registers.BAUD_RATE, value)

    @property
    def return_delay(self):
        return self._rb(registers.RETURN_DELAY)

    @return_delay.setter
    def return_delay(self, value):
        self._wb(registers.RETURN_DELAY, value)

    @property
    def cw_angle_limit(self):
        return self._rw(registers.CW_ANGLE_LIMIT)

    @cw_angle_limit.setter
    def cw_angle_limit(self, value):
        self._ww(registers.CW_ANGLE_LIMIT, value)

    @property
    def ccw_angle_limit(self):
        return self._rw(registers.CCW_ANGLE_LIMIT)

    @ccw_angle_limit.setter
    def ccw_angle_limit(self, value):
        self._ww(registers.CCW_ANGLE_LIMIT, value)

    @property
    def temp_limit(self):
        return self._rb(registers.TEMP_LIMIT)

    @temp_limit.setter
    def temp_limit(self, value):
        self._wb(registers.TEMP_LIMIT, value)

    @property
    def min_voltage_limit(self):
        return self._rb(registers.MIN_VOLTAGE_LIMIT)

    @min_voltage_limit.setter
    def min_voltage_limit(self, value):
        self._wb(registers.MIN_VOLTAGE_LIMIT, value)

    @property
    def max_voltage_limit(self):
        return self._rb(registers.MAX_VOLTAGE_LIMIT)

    @max_voltage_limit.setter
    def max_voltage_limit(self, value):
        self._wb(registers.MAX_VOLTAGE_LIMIT, value)

    @property
    def max_torque(self):
        return self._rw(registers.MAX_TORQUE)

    @max_torque.setter
    def max_torque(self, value):
        self._ww(registers.MAX_TORQUE, value)

    @property
    def status_return_level(self):
        return self._rb(registers.STATUS_RETURN_LEVEL)

    @status_return_level.setter
    def status_return_level(self, value):
        self._wb(registers.STATUS_RETURN_LEVEL, value)

    @property
    def alarm_led(self):
        return self._rb(registers.ALARM_LED)

    @alarm_led.setter
    def alarm_led(self, value):
        self._wb(registers.ALARM_LED, value)

    @property
    def alarm_shutdown(self):
        return self._rb(registers.ALARM_SHUTDOWN)

    @alarm_shutdown.setter
    def alarm_shutdown(self, value):
        self._wb(registers.ALARM_SHUTDOWN, value)

    @property
    def torque_enable(self):
        return self._rb(registers.TORQUE_ENABLE)

    @torque_enable.setter
    def torque_enable(self, value):
        self._wb(registers.TORQUE_ENABLE, value)

    @property
    def led(self):
        return self._rb(registers.LED)

    @led.setter
    def led(self, value):
        self._wb(registers.LED, value)

    @property
    def cw_compliance_margin(self):
        return self._rb(registers.CW_COMPLIANCE_MARGIN)

    @cw_compliance_margin.setter
    def cw_compliance_margin(self, value):
        self._wb(registers.CW_COMPLIANCE_MARGIN, value)

    @property
    def ccw_compliance_margin(self):
        return self._rb(registers.CCW_COMPLIANCE_MARGIN)

    @ccw_compliance_margin.setter
    def ccw_compliance_margin(self, value):
        self._wb(registers.CCW_COMPLIANCE_MARGIN, value)

    @property
    def cw_compliance_slope(self):
        return self._rb(registers.CW_COMPLIANCE_SLOPE)

    @cw_compliance_slope.setter
    def cw_compliance_slope(self, value):
        self._wb(registers.CW_COMPLIANCE_SLOPE, value)

    @property
    def ccw_compliance_slope(self):
        return self._rb(registers.CCW_COMPLIANCE_SLOPE)

    @ccw_compliance_slope.setter
    def ccw_compliance_slope(self, value):
        self._wb(registers.CCW_COMPLIANCE_SLOPE, value)

    @property
    def goal_position(self):
        return self._rw(registers.GOAL_POSITION)

    @goal_position.setter
    def goal_position(self, value):
        self._ww(registers.GOAL_POSITION, value)

    @property
    def moving_speed(self):
        return self._rw(registers.MOVING_SPEED)

    @moving_speed.setter
    def moving_speed(self, value):
        self._ww(registers.MOVING_SPEED, value)

    @property
    def torque_limit(self):
        return self._rw(registers.TORQUE_LIMIT)

    @torque_limit.setter
    def torque_limit(self, value):
        self._ww(registers.TORQUE_LIMIT, value)

    @property
    def present_position(self):
        return self._rw(registers.PRESENT_POSITION)

    @property
    def present_speed(self):
        return self._rw(registers.PRESENT_SPEED)

    @property
    def present_load(self):
        return self._rw(registers.PRESENT_LOAD)

    @property
    def present_voltage(self):
        return self._rb(registers.PRESENT_VOLTAGE)

    @property
    def present_temperature(self):
        return self._rb(registers.PRESENT_TEMPERATURE)

    @property
    def registered(self):
        return self._rb(registers.REGISTERED)

    @property
    def moving(self):
        return bool(self._rb(registers.MOVING))

    @property
    def lock(self):
        return self._rb(registers.LOCK)

    @lock.setter
    def lock(self, value):
        self._wb(registers.LOCK, value)

    @property
    def punch(self):
        return self._rw(registers.PUNCH)

    @punch.setter
    def punch(self, value):
        self._ww(registers.PUNCH, value)
