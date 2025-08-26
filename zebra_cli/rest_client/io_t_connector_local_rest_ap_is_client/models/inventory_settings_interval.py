from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.inventory_settings_interval_unit import check_inventory_settings_interval_unit
from ..models.inventory_settings_interval_unit import InventorySettingsIntervalUnit
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="InventorySettingsInterval")



@_attrs_define
class InventorySettingsInterval:
    """ The time interval (how often) to report each tag

        Attributes:
            unit (Union[Unset, InventorySettingsIntervalUnit]):
            value (Union[Unset, int]):
     """

    unit: Union[Unset, InventorySettingsIntervalUnit] = UNSET
    value: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        unit: Union[Unset, str] = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit


        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if unit is not UNSET:
            field_dict["unit"] = unit
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _unit = d.pop("unit", UNSET)
        unit: Union[Unset, InventorySettingsIntervalUnit]
        if isinstance(_unit,  Unset):
            unit = UNSET
        else:
            unit = check_inventory_settings_interval_unit(_unit)




        value = d.pop("value", UNSET)

        inventory_settings_interval = cls(
            unit=unit,
            value=value,
        )


        inventory_settings_interval.additional_properties = d
        return inventory_settings_interval

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
