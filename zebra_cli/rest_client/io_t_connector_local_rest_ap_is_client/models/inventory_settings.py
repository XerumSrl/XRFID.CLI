from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.inventory_settings_interval import InventorySettingsInterval





T = TypeVar("T", bound="InventorySettings")



@_attrs_define
class InventorySettings:
    """ Reader settings for inventory mode. If absent, the reader will report each tag on each antenna once per minute.

        Attributes:
            interval (Union[Unset, InventorySettingsInterval]): The time interval (how often) to report each tag
     """

    interval: Union[Unset, 'InventorySettingsInterval'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.inventory_settings_interval import InventorySettingsInterval
        interval: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if interval is not UNSET:
            field_dict["interval"] = interval

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inventory_settings_interval import InventorySettingsInterval
        d = dict(src_dict)
        _interval = d.pop("interval", UNSET)
        interval: Union[Unset, InventorySettingsInterval]
        if isinstance(_interval,  Unset):
            interval = UNSET
        else:
            interval = InventorySettingsInterval.from_dict(_interval)




        inventory_settings = cls(
            interval=interval,
        )


        inventory_settings.additional_properties = d
        return inventory_settings

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
