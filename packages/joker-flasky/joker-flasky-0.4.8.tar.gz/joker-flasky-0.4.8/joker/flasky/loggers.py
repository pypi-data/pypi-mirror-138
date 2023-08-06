#!/usr/bin/env python3
# coding: utf-8

"""
This module is deprecated.
"""

import warnings
from joker.redis.loggers import RedisHandler, ErrorInterface

warnings.warn(
    "joker.flasky.loggers is deprecated. Use joker.redis.loggers instead.",
    DeprecationWarning,
)

_compat = [
    RedisHandler,
    ErrorInterface,
]

__all__ = []
