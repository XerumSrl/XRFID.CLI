from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ActionBlinkConfiguration")



@_attrs_define
class ActionBlinkConfiguration:
    """ action blink configuration for GPO or LED

        Attributes:
            on (float): SET GPO or LED to desired state for ON (milliseconds) duration
            off (float): Toggle GPO or LED for OFF(milliseconds) duration
            duration (float): Total duration in milliseconds to perform blink. 0 will blink GPO or LED forever
     """

    on: float
    off: float
    duration: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        on = self.on

        off = self.off

        duration = self.duration


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ON": on,
            "OFF": off,
            "DURATION": duration,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        on = d.pop("ON")

        off = d.pop("OFF")

        duration = d.pop("DURATION")

        action_blink_configuration = cls(
            on=on,
            off=off,
            duration=duration,
        )


        action_blink_configuration.additional_properties = d
        return action_blink_configuration

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
