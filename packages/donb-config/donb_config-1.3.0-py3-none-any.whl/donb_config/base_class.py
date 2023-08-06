# -*- coding: utf-8 -*-

import dataclasses
from typing import Any


@dataclasses.dataclass
class ConfigBase:
    def __post_init__(self) -> None:
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            value = self._convert_fields(field, value)
            if not isinstance(value, field.type):
                raise TypeError(
                    f"Expected {field.name} to be {field.type}, " f"got {repr(value)}"
                )

    def _convert_fields(self, field: dataclasses.Field, value: Any) -> Any:
        try:
            value = field.type(value)
        except TypeError:
            value = field.type(**value)
        except ValueError:
            pass
        setattr(self, field.name, value)
        return value
