from typing import Any, Dict, List, Union

JNode = Union[str, int, float, None, List[Any], Dict[str, Any]]
JObj = Dict[str, JNode]

# Annotation keys
DESCRIPTION_KEY = "description"
TITLE_KEY = "title"
DEFAULT_KEY = "default"
EXAMPLES_KEY = "examples"
DEPRECATED_KEY = "deprecated"
READONLY_KEY = "readOnly"
WRITEONLY_KEY = "writeOnly"

# Object keys
REQUIRED_KEY = "required"
PROPERTIES_KEY = "properties"
TYPE_KEY = "type"
ADDITIONAL_PROPERTIES_KEY = "additionalProperties"

# Array keys
ITEMS_KEY = "items"

# String constraint keys
MIN_LENGTH_KEY = "minLength"
MAX_LENGTH_KEY = "maxLength"
PATTERN_KEY = "pattern"
FORMAT_KEY = "format"

STRING_CONSTRAINT_KEYS = (
    MIN_LENGTH_KEY,
    MAX_LENGTH_KEY,
    PATTERN_KEY,
    FORMAT_KEY,
)

# Number constraint keys
MULTIPLE_OF_KEY = "multipleOf"
MIN_KEY = "minimum"
MAX_KEY = "maximum"
EXCLUSIVE_MIN_KEY = "exclusiveMinimum"
EXCLUSIVE_MAX_KEY = "exclusiveMaximum"

NUMBER_CONSTRAINT_KEYS = (
    MULTIPLE_OF_KEY,
    MIN_KEY,
    MAX_KEY,
    EXCLUSIVE_MIN_KEY,
    EXCLUSIVE_MAX_KEY,
)

# Schema composition keys
ONE_OF_KEY = "oneOf"
ANY_OF_KEY = "anyOf"
ALL_OF_KEY = "allOf"

COMPOSITION_KEYS = (
    ONE_OF_KEY,
    ANY_OF_KEY,
    ALL_OF_KEY,
)

# Reference key
REFERENCE_KEY = "$ref"

# Type keys
ARRAY_TYPE = "array"
OBJECT_TYPE = "object"
STRING_TYPE = "string"
NUMBER_TYPE = "number"
INTEGER_TYPE = "integer"
BOOLEAN_TYPE = "boolean"
NULL_TYPE = "null"
ENUM_TYPE = "enum"

VALUE_TYPES = (
    STRING_TYPE,
    NUMBER_TYPE,
    INTEGER_TYPE,
    BOOLEAN_TYPE,
    NULL_TYPE,
)

# Miscellaneous
SPACE = "&nbsp;"
