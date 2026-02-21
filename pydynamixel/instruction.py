#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Protocol 1.0 instruction constants."""


class INSTRUCTION:
    PING = 0x01
    READ_DATA = 0x02
    WRITE_DATA = 0x03
    REG_WRITE = 0x04
    ACTION = 0x05
    RESET = 0x06
    SYNC_WRITE = 0x83