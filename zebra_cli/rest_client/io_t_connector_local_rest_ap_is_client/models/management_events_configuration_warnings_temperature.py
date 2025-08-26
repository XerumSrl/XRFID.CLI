from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagementEventsConfigurationWarningsTemperature")



@_attrs_define
class ManagementEventsConfigurationWarningsTemperature:
    """ Reader temperature warning limits

        Attributes:
            ambient (float): Ambient temperature limit Default: 75.0.
            pa (float): PA temperature limit Default: 105.0.
     """

    ambient: float = 75.0
    pa: float = 105.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ambient = self.ambient

        pa = self.pa


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ambient": ambient,
            "pa": pa,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ambient = d.pop("ambient")

        pa = d.pop("pa")

        management_events_configuration_warnings_temperature = cls(
            ambient=ambient,
            pa=pa,
        )


        management_events_configuration_warnings_temperature.additional_properties = d
        return management_events_configuration_warnings_temperature

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
