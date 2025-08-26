from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="CpuStats")



@_attrs_define
class CpuStats:
    """ System CPU Statistics

        Attributes:
            user (Union[Unset, int]): User processes CPU utilization percentage Example: 42.
            system (Union[Unset, int]): System processes CPU utilization percentage Example: 32.
     """

    user: Union[Unset, int] = UNSET
    system: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        user = self.user

        system = self.system


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if user is not UNSET:
            field_dict["user"] = user
        if system is not UNSET:
            field_dict["system"] = system

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user = d.pop("user", UNSET)

        system = d.pop("system", UNSET)

        cpu_stats = cls(
            user=user,
            system=system,
        )


        cpu_stats.additional_properties = d
        return cpu_stats

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
