#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Response object for Dynamixel status packets."""

from dataclasses import dataclass
from typing import List


@dataclass
class Response:
    """Decoded status packet."""

    servo_id: int
    error: int
    data: List[int]
    checksum_match: bool

    def get_error(self):
        return self.error > 0 or not self.checksum_match

    def get_error_str(self):
        if self.error > 0:
            return f"Error code {self.error}"
        if not self.checksum_match:
            return "Checksum mismatch."
        return None
