from __future__ import annotations
import inspect
import os

from typing import TYPE_CHECKING, Callable, TypeVar

import discord
from discord.components import Component, Button as ButtonComponent, SelectMenu as SelectComponent
from discord.ui.item import ItemCallbackType

from .components import TextInput as TextInputComponent
from .enums import TextInputStyle

V = TypeVar("V", bound="Modal")

if TYPE_CHECKING:
    from typing import Any

def _component_to_item(component: Component) -> discord.ui.Item:
    if isinstance(component, ButtonComponent):
        from discord.ui.button import Button
        return Button.from_component(component)

    if isinstance(component, SelectComponent):
        from discord.ui.select import Select
        return Select.from_component(component)

    if isinstance(component, TextInputComponent):
        return TextInput.from_component(component)

    return discord.ui.Item.from_component(component)

discord.ui.view._component_to_item = _component_to_item

class TextInput(discord.ui.Item[V]):
    __item_repr_attributes__: tuple[str, ...] = (
        "style",
        "label",
        "min_length",
        "max_length"
    )

    def __init__(self, *,
        label: str,
        style: TextInputStyle,
        custom_id: str | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        required: bool = False,
        default_value: str | None = None,
        placeholder: str | None = None,
        row: int | None = None
    ) -> None:
        super().__init__()
        self._provided_custom_id = custom_id is not None
        if custom_id is None:
            custom_id = os.urandom(16).hex()
        
        if min_length is not None and min_length < 0:
            raise ValueError("min_length must be greater or equal to 0")
        
        if max_length is not None and (max_length > 4000 or max_length < 1):
            raise ValueError("max_length must be lower or equal to 4000 and greater or equal to 1")

        self._underlying = TextInputComponent._raw_construct(
            style = style,
            custom_id = custom_id,
            label = label,
            required = required,
            default_value = default_value,
            placeholder = placeholder,
            min_length = min_length,
            max_length = max_length
        )
        self.row = row

    @property
    def width(self) -> int:
        return 5

    @property
    def style(self) -> TextInputStyle:
        return self._underlying.style

    @style.setter
    def style(self, value: TextInputStyle):
        self._underlying.style = value

    @property
    def custom_id(self) -> str | None:
        return self._underlying.custom_id

    @custom_id.setter
    def custom_id(self, value: str | None):
        self._underlying.custom_id = value

    @property
    def label(self) -> str:
        return self._underlying.label

    @label.setter
    def label(self, value: str):
        self._underlying.label = value

    @property
    def min_length(self) -> int | None:
        return self._underlying.min_length

    @min_length.setter
    def min_length(self, value: int | None):
        self._underlying.min_length = value

    @property
    def max_length(self) -> int | None:
        return self._underlying.max_length

    @max_length.setter
    def max_length(self, value: int | None):
        self._underlying.max_length = value

    @property
    def default_value(self) -> str | None:
        return self._underlying.default_value

    @default_value.setter
    def default_value(self, value: str | None):
        self._underlying.default_value = value

    @property
    def placeholder(self) -> str | None:
        return self._underlying.placeholder

    @placeholder.setter
    def placeholder(self, value: str | None):
        self._underlying.placeholder = value

    @property
    def required(self) -> bool:
        return self._underlying.required

    @required.setter
    def required(self, value: bool):
        self._underlying.required = value

    @classmethod
    def from_component(cls: type[TextInput], component: TextInputComponent) -> TextInput:
        return cls(
            label = component.label,
            style = component.style,
            custom_id = component.custom_id,
            min_length = component.min_length,
            max_length = component.max_length,
            required = component.required,
            default_value = component.default_value,
            placeholder = component.placeholder,
            row = None
        )
        
    def to_component_dict(self) -> dict[str, Any]:
        return self._underlying.to_dict()

    def refresh_component(self, component: TextInputComponent) -> None:
        self._underlying = component

def text_input(*,
    label: str,
    style: TextInputStyle,
    custom_id: str | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    required: bool = False,
    default_value: str | None = None,
    placeholder: str | None = None
) -> Callable[[ItemCallbackType], ItemCallbackType]:
    def decorator(func: ItemCallbackType) -> ItemCallbackType:
        if not inspect.iscoroutinefunction(func):
            raise TypeError("text_input callback must be a coroutine function")
        
        func.__discord_ui_model_type__ = TextInput
        func.__discord_ui_model_kwargs__ = {
            "label": label,
            "style": style,
            "custom_id": custom_id,
            "min_length": min_length,
            "max_length": max_length,
            "required": required,
            "default_value": default_value,
            "placeholder": placeholder
        }
        return func
    return decorator

class Modal(discord.ui.View):
    pass