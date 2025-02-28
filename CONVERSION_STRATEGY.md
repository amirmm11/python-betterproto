# Strategy for Converting betterproto to Standard Library Types

## Overview

This document outlines the strategy for modifying betterproto to use standard library types (dataclasses and enums) instead of custom implementations, eliminating the extra serialization, type checking, and runtime logic.

## Core Modifications

### 1. Enum Implementation (`src/betterproto/enum.py`)

Replace the custom `Enum` class with Python's standard `enum.IntEnum`:

```python
# Current implementation
class Enum(IntEnum if TYPE_CHECKING else int, metaclass=EnumType):
    # Custom implementation...

# Modified implementation
class Enum(enum.IntEnum):
    """Base class for protobuf enumerations that simply inherits from standard IntEnum."""
    pass
```

### 2. Message Implementation (`src/betterproto/__init__.py`)

Replace the custom `Message` class with a dataclass-compatible implementation:

```python
# Current implementation
class Message(ABC):
    # Complex implementation with serialization, deserialization, etc.

# Modified implementation
class Message:
    """Simple base class for protocol buffer messages using standard dataclasses."""
    
    def __post_init__(self):
        """Minimal post initialization."""
        pass
```

### 3. Field Definitions (`src/betterproto/__init__.py`)

Modify field definition functions to use standard dataclass fields:

```python
def dataclass_field(number, proto_type, **kwargs):
    """Simplified field that only stores protobuf metadata as needed."""
    return dataclasses.field(
        default=None if kwargs.get('optional', False) else dataclasses.MISSING,
        metadata={"betterproto_field_number": number}
    )
```

### 4. Templates (`src/betterproto/templates/template.py.j2`)

Update the code generation templates to generate standard Python classes:

```jinja
{% for enum in output_file.enums %}
class {{ enum.py_name }}(enum.IntEnum):
    {% for entry in enum.entries %}
    {{ entry.name }} = {{ entry.value }}
    {% endfor %}
{% endfor %}

{% for message in output_file.messages %}
@dataclasses.dataclass
class {{ message.py_name }}:
    {% for field in message.fields %}
    {{ field.name }}: {{ field.type_hint }} = dataclasses.field(default=None)
    {% endfor %}
{% endfor %}
```

## Serialization Strategy

Create a separate utility module for serialization/deserialization that works with standard dataclasses:

```python
def serialize_message(message: Any) -> bytes:
    """External serialization function for standard dataclasses."""
    # Implementation that uses protobuf wire format
    pass

def deserialize_message(message_class: Type, data: bytes) -> Any:
    """External deserialization function for standard dataclasses."""
    # Implementation that creates instances of standard dataclasses
    pass
```

## Implementation Steps

1. Create a simplified `StandardMessage` class that inherits from nothing
2. Create a simplified `StandardEnum` class that inherits from `enum.IntEnum`
3. Modify code generation templates to use these classes
4. Create external serialization utilities that operate on standard classes
5. Update all import paths and references throughout the codebase

This approach maintains compatibility with the Protocol Buffer standard while simplifying the runtime implementation.