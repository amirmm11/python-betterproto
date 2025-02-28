# Comparison: Standard Library vs. BetterProto

## Overview

This document compares the standard library approach to betterproto's original implementation, highlighting the differences and benefits of each approach.

## Implementation Differences

### Enum Implementation

**BetterProto Original:**
```python
class Enum(IntEnum if TYPE_CHECKING else int, metaclass=EnumType):
    # Complex implementation with custom metaclass
    # Special serialization/deserialization behavior
    # Custom try_value method that creates values on the fly
```

**Standard Library:**
```python
class Status(enum.IntEnum):
    UNKNOWN = 0
    ACTIVE = 1
    INACTIVE = 2
```

### Message Implementation

**BetterProto Original:**
```python
@dataclasses.dataclass(eq=False, repr=False)
class Person(betterproto.Message):
    name: str = betterproto.string_field(1)
    age: int = betterproto.int32_field(2)
    status: Status = betterproto.enum_field(3)
    tags: List[str] = betterproto.string_field(4, repeated=True)
    address: Optional["Address"] = betterproto.message_field(5)
    
    # Inherits complex serialization/deserialization methods
    # Special equality and representation behavior
    # Wire format encoding/decoding
```

**Standard Library:**
```python
@dataclasses.dataclass
class Person:
    name: str = None
    age: int = None
    status: Status = None
    tags: List[str] = dataclasses.field(default_factory=list)
    address: Optional[Address] = None
```

## Feature Comparison

| Feature | BetterProto | Standard Library |
|---------|------------|-----------------|
| Wire Format Serialization | ✅ Built-in | ❌ Would need external utility |
| JSON Serialization | ✅ Built-in | ✅ Via dataclasses.asdict() |
| Type Checking | ✅ Runtime checks | ❌ Static only |
| Memory Usage | ❓ Higher (metadata) | ✅ Lower |
| Performance | ❓ Slower (validations) | ✅ Faster |
| Complexity | ❌ Higher | ✅ Lower |
| IDE Support | ✅ Good | ✅ Excellent |
| Maintainability | ❌ Complex | ✅ Simple |

## Use Case Recommendations

**Use BetterProto When:**
- You need built-in wire format serialization/deserialization
- Protocol buffer compatibility is critical
- You want runtime type checking and validation
- The additional functionality outweighs the performance cost

**Use Standard Library When:**
- You only need the structural definitions
- Performance and memory usage are critical
- You prefer simplicity and standard library compatibility
- You're willing to handle any needed serialization separately

## Implementation Strategy

To switch to the standard library approach:

1. Replace custom enum classes with standard `enum.IntEnum`
2. Replace custom message classes with standard `@dataclasses.dataclass`
3. Replace field definitions with standard dataclass fields
4. Update template generation to use standard types
5. Create separate utilities for any needed serialization

This approach provides a cleaner, more maintainable codebase with better performance at the cost of some built-in functionality.