from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="GPIOLEDConfigurationGPIDebounce")



@_attrs_define
class GPIOLEDConfigurationGPIDebounce:
    """ GPI Debounce Configuration

        Attributes:
            1 (Union[Unset, float]): GPI Debounce for pin 1 in milliseconds Default: 50.0.
            2 (Union[Unset, float]): GPI Debounce for pin 2 in milliseconds Default: 50.0.
            3 (Union[Unset, float]): GPI Debounce for pin 3 in milliseconds (only applicable to FX9600 readers) Default:
                50.0.
            4 (Union[Unset, float]): GPI Debounce for pin 4 in milliseconds (only applicable to FX9600 readers) Default:
                50.0.
     """

    1: Union[Unset, float] = 50.0
    2: Union[Unset, float] = 50.0
    3: Union[Unset, float] = 50.0
    4: Union[Unset, float] = 50.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        1 = self.1

        2 = self.2

        3 = self.3

        4 = self.4


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if 1 is not UNSET:
            field_dict["1"] = 1
        if 2 is not UNSET:
            field_dict["2"] = 2
        if 3 is not UNSET:
            field_dict["3"] = 3
        if 4 is not UNSET:
            field_dict["4"] = 4

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        1 = d.pop("1", UNSET)

        2 = d.pop("2", UNSET)

        3 = d.pop("3", UNSET)

        4 = d.pop("4", UNSET)

        gpioled_configuration_gpi_debounce = cls(
            1=1,
            2=2,
            3=3,
            4=4,
        )


        gpioled_configuration_gpi_debounce.additional_properties = d
        return gpioled_configuration_gpi_debounce

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
