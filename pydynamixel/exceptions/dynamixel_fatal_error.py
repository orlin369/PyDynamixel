#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Fatal Dynamixel protocol exception type."""


class DynamixelFatalError(Exception):
    """Raised when a servo reports an error bit in the status packet."""
