from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gpioled_configuration_gpo_defaults_1 import check_gpioled_configuration_gpo_defaults_1
from ..models.gpioled_configuration_gpo_defaults_1 import GPIOLEDConfigurationGPODefaults1
from ..models.gpioled_configuration_gpo_defaults_2 import check_gpioled_configuration_gpo_defaults_2
from ..models.gpioled_configuration_gpo_defaults_2 import GPIOLEDConfigurationGPODefaults2
from ..models.gpioled_configuration_gpo_defaults_3 import check_gpioled_configuration_gpo_defaults_3
from ..models.gpioled_configuration_gpo_defaults_3 import GPIOLEDConfigurationGPODefaults3
from ..models.gpioled_configuration_gpo_defaults_4 import check_gpioled_configuration_gpo_defaults_4
from ..models.gpioled_configuration_gpo_defaults_4 import GPIOLEDConfigurationGPODefaults4
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="GPIOLEDConfigurationGPODefaults")



@_attrs_define
class GPIOLEDConfigurationGPODefaults:
    """ GPO default configurations

        Attributes:
            1 (Union[Unset, GPIOLEDConfigurationGPODefaults1]): set default state for GPO pin 1
            2 (Union[Unset, GPIOLEDConfigurationGPODefaults2]): set default state for GPO pin 2
            3 (Union[Unset, GPIOLEDConfigurationGPODefaults3]): set default state for GPO pin 3
            4 (Union[Unset, GPIOLEDConfigurationGPODefaults4]): set default state for GPO pin 4
     """

    1: Union[Unset, GPIOLEDConfigurationGPODefaults1] = UNSET
    2: Union[Unset, GPIOLEDConfigurationGPODefaults2] = UNSET
    3: Union[Unset, GPIOLEDConfigurationGPODefaults3] = UNSET
    4: Union[Unset, GPIOLEDConfigurationGPODefaults4] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        1: Union[Unset, str] = UNSET
        if not isinstance(self.1, Unset):
            1 = self.1


        2: Union[Unset, str] = UNSET
        if not isinstance(self.2, Unset):
            2 = self.2


        3: Union[Unset, str] = UNSET
        if not isinstance(self.3, Unset):
            3 = self.3


        4: Union[Unset, str] = UNSET
        if not isinstance(self.4, Unset):
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
        _1 = d.pop("1", UNSET)
        1: Union[Unset, GPIOLEDConfigurationGPODefaults1]
        if isinstance(_1,  Unset):
            1 = UNSET
        else:
            1 = check_gpioled_configuration_gpo_defaults_1(_1)




        _2 = d.pop("2", UNSET)
        2: Union[Unset, GPIOLEDConfigurationGPODefaults2]
        if isinstance(_2,  Unset):
            2 = UNSET
        else:
            2 = check_gpioled_configuration_gpo_defaults_2(_2)




        _3 = d.pop("3", UNSET)
        3: Union[Unset, GPIOLEDConfigurationGPODefaults3]
        if isinstance(_3,  Unset):
            3 = UNSET
        else:
            3 = check_gpioled_configuration_gpo_defaults_3(_3)




        _4 = d.pop("4", UNSET)
        4: Union[Unset, GPIOLEDConfigurationGPODefaults4]
        if isinstance(_4,  Unset):
            4 = UNSET
        else:
            4 = check_gpioled_configuration_gpo_defaults_4(_4)




        gpioled_configuration_gpo_defaults = cls(
            1=1,
            2=2,
            3=3,
            4=4,
        )


        gpioled_configuration_gpo_defaults.additional_properties = d
        return gpioled_configuration_gpo_defaults

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
