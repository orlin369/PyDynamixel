#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Dynamixel protocol error bit masks."""


class ERROR_BIT_MASKS:
    INPUT_VOLTAGE = 0x01
    ANGLE_LIMIT = 0x02
    OVERHEATING = 0x04
    RANGE = 0x08
    SEND_CHECKSUM = 0x10
    OVERLOAD = 0x20
    INSTRUCTION = 0x40