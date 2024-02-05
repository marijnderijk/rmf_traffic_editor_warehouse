from typing import Any

class ParamValue():
    UNDEFINED: int = 0
    STRING: int = 1
    INT: int = 2
    DOUBLE: int = 3
    BOOL: int = 4

    def __init__(self, type: int, value: Any):
        self.type = int(type)
        self.value = value

    TYPE_MAPPING: dict = {
        UNDEFINED: lambda x: None,
        STRING: str,
        INT: int,
        DOUBLE: float,
        BOOL: bool,
    }

    @classmethod
    def from_yaml(cls, yaml_value):
        """
        Create a ParamValue from a YAML node.
        :param yaml_value: [type, raw_value] where type is one of the ParamValue types
        :return: A ParamValue object.
        """
        value_type, raw_value = yaml_value
        if value_type not in cls.TYPE_MAPPING:
            raise ValueError(f"Unsupported ParamValue type: {value_type}")

        value_constructor = cls.TYPE_MAPPING[value_type]
        value = value_constructor(raw_value)
        return cls(type=value_type, value=value)

    def to_yaml(self):
        return [self.type, self.value]

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash(self.value)
