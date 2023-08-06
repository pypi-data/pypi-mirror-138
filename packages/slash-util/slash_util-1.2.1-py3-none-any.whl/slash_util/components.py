from __future__ import annotations
from typing import Any, ClassVar

import discord
from discord.enums import try_enum

from .enums import TextInputStyle

class TextInput(discord.Component):
    __slots__: tuple[str, ...] = (
        "style",
        "custom_id",
        "label",
        "min_length",
        "max_length",
        "default_value",
        "placeholder",
        "required"
    )

    __repr_info__: ClassVar[tuple[str, ...]] = __slots__

    def __init__(self, data: dict[str, Any]):
        self.type = try_enum(discord.ComponentType, 4)
        self.style: TextInputStyle = try_enum(TextInputStyle, data['style'])
        self.custom_id: str | None = data.get("custom_id")
        self.label: str = data["label"]
        self.min_length: int | None = data.get("min_length")
        self.max_length: int | None = data.get("max_length")
        self.default_value: str | None = data.get("default_value")
        self.placeholder: str | None = data.get("placeholder")
        self.required: bool = data.get("required", False)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "type": 4,
            "style": self.style.value,
            "label": self.label,
            "required": self.required
        }

        if self.min_length is not None:
            payload['min_length'] = self.min_length
        if self.max_length is not None:
            payload['max_length'] = self.max_length

        if self.custom_id is not None:
            payload['custom_id'] = self.custom_id
        
        if self.default_value is not None:
            payload['default_value'] = self.default_value
        
        if self.placeholder is not None:
            payload['placeholder'] = self.placeholder
        
        return payload
