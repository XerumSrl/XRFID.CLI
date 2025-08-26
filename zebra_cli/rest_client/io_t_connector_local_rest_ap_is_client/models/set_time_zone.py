from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.set_time_zone_time_zone import check_set_time_zone_time_zone
from ..models.set_time_zone_time_zone import SetTimeZoneTimeZone
from typing import cast






T = TypeVar("T", bound="SetTimeZone")



@_attrs_define
class SetTimeZone:
    """ Set Reader Time Zone

        Attributes:
            time_zone (SetTimeZoneTimeZone): Allowed time zones on the reader
     """

    time_zone: SetTimeZoneTimeZone
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        time_zone: str = self.time_zone


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "timeZone": time_zone,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        time_zone = check_set_time_zone_time_zone(d.pop("timeZone"))




        set_time_zone = cls(
            time_zone=time_zone,
        )


        set_time_zone.additional_properties = d
        return set_time_zone

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
