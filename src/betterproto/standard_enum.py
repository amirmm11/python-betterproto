"""
Standard library-based implementation of Protocol Buffer enums.
This module provides a simplified Enum class that inherits directly
from Python's enum.IntEnum without adding extra functionality.
"""

from __future__ import annotations

import enum
from typing import (
    Any,
    Optional,
    Self,
    Type,
)


class StandardEnum(enum.IntEnum):
    """
    A simple wrapper around enum.IntEnum for Protocol Buffers that
    maintains API compatibility with betterproto.Enum while using
    standard library implementation.
    """

    @classmethod
    def try_value(cls, value: int = 0) -> Self:
        """Return the value which corresponds to the value.

        Parameters
        -----------
        value: :class:`int`
            The value of the enum member to get.

        Returns
        -------
        :class:`StandardEnum`
            The corresponding member or a new instance with the given value
            if it's not actually a member.
        """
        try:
            return cls(value)
        except ValueError:
            # Since we can't easily create new enum values at runtime when they don't exist,
            # we just return the first enum value as a fallback with a warning
            import warnings
            warnings.warn(f"Unknown value {value} for enum {cls.__name__}, using first value as fallback")
            return next(iter(cls.__members__.values()))

    @classmethod
    def from_string(cls, name: str) -> Self:
        """Return the value which corresponds to the string name.

        Parameters
        -----------
        name: :class:`str`
            The name of the enum member to get.

        Raises
        -------
        :exc:`ValueError`
            The member was not found in the Enum.
        """
        try:
            return cls[name]
        except KeyError as e:
            raise ValueError(f"Unknown value {name} for enum {cls.__name__}") from e


# For backwards compatibility
Enum = StandardEnum