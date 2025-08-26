from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MemoryStats")



@_attrs_define
class MemoryStats:
    """ System memory statistics

        Attributes:
            total (Union[Unset, int]): Total RAM in bytes Example: 26098076.
            free (Union[Unset, int]): Free RAM in bytes Example: 195612672.
            used (Union[Unset, int]): Used RAM in bytes Example: 65368064.
     """

    total: Union[Unset, int] = UNSET
    free: Union[Unset, int] = UNSET
    used: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        total = self.total

        free = self.free

        used = self.used


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if total is not UNSET:
            field_dict["total"] = total
        if free is not UNSET:
            field_dict["free"] = free
        if used is not UNSET:
            field_dict["used"] = used

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total", UNSET)

        free = d.pop("free", UNSET)

        used = d.pop("used", UNSET)

        memory_stats = cls(
            total=total,
            free=free,
            used=used,
        )


        memory_stats.additional_properties = d
        return memory_stats

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
