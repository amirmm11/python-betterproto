"""
Standard library-based implementation of Protocol Buffer messages.
This module provides a simplified Message class that uses standard Python
dataclasses without adding complex serialization or deserialization logic.
"""

from __future__ import annotations

import dataclasses
import json
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Type,
    get_type_hints,
)


@dataclasses.dataclass
class StandardMessage:
    """
    A simple base class for Protocol Buffer messages that uses standard Python
    dataclasses rather than custom serialization/deserialization.
    
    This class intentionally lacks the serialization, type checking, and other
    behaviors from the full betterproto.Message class, providing just structure.
    """
    
    def __post_init__(self) -> None:
        """Minimal post-initialization that can be overridden by subclasses."""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary for easy JSON serialization.
        This is a simple wrapper around dataclasses.asdict() with datetime handling.
        """
        def _convert(obj):
            if isinstance(obj, StandardMessage):
                return {k: _convert(v) for k, v in dataclasses.asdict(obj).items()}
            elif isinstance(obj, list):
                return [_convert(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: _convert(v) for k, v in obj.items()}
            elif isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, timedelta):
                return str(obj.total_seconds()) + 's'
            else:
                return obj
        
        return _convert(self)
    
    def to_json(self) -> str:
        """Convert the message to a JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StandardMessage:
        """
        Create a message from a dictionary.
        This is a simple implementation for standard dataclasses.
        """
        field_types = get_type_hints(cls)
        
        # Process the data to convert nested dictionaries to appropriate message types
        processed_data = {}
        for field_name, field_value in data.items():
            if field_name in field_types:
                field_type = field_types[field_name]
                
                # Handle nested messages
                if (isinstance(field_value, dict) and 
                    hasattr(field_type, "__origin__") and 
                    field_type.__origin__ is not dict):
                    # This is a nested message type
                    processed_data[field_name] = field_type.from_dict(field_value)
                else:
                    processed_data[field_name] = field_value
        
        return cls(**processed_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> StandardMessage:
        """Create a message from a JSON string."""
        return cls.from_dict(json.loads(json_str))


# For backwards compatibility
Message = StandardMessage


def dataclass_field(
    number: int,
    proto_type: str,
    *,
    map_types: Optional[tuple[str, str]] = None,
    group: Optional[str] = None,
    wraps: Optional[str] = None,
    optional: bool = False,
) -> dataclasses.Field:
    """
    Creates a standard dataclass field with minimal metadata for Protocol Buffers.
    
    This is a simplified version that only stores the field number and type for
    documentation purposes, but doesn't add the extra serialization metadata.
    """
    return dataclasses.field(
        default=None if optional else dataclasses.MISSING,
        metadata={
            "betterproto_field_number": number,
            "betterproto_proto_type": proto_type,
        },
    )


# Create simple field creation functions that just pass through to dataclass_field
def enum_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "enum", group=group, optional=optional)

def bool_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "bool", group=group, optional=optional)

def int32_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "int32", group=group, optional=optional)

def int64_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "int64", group=group, optional=optional)

def uint32_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "uint32", group=group, optional=optional)

def uint64_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "uint64", group=group, optional=optional)

def string_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "string", group=group, optional=optional)

def bytes_field(number: int, group: Optional[str] = None, optional: bool = False) -> Any:
    return dataclass_field(number, "bytes", group=group, optional=optional)

def message_field(
    number: int,
    group: Optional[str] = None,
    wraps: Optional[str] = None,
    optional: bool = False,
) -> Any:
    return dataclass_field(number, "message", group=group, wraps=wraps, optional=optional)

def map_field(number: int, key_type: str, value_type: str, group: Optional[str] = None) -> Any:
    return dataclass_field(number, "map", map_types=(key_type, value_type), group=group)