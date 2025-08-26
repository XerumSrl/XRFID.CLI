from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="EachReadPoint")



@_attrs_define
class EachReadPoint:
    """ Adjust cable loss compensation per read point labeled 1,2,3... upto max supported read points

        Attributes:
            cable_length (int): Cable Length Field. Accepts float values Example: 1.
            cable_loss_per_hundred_ft (int): Cable Loss per Hundred Feet. Accepts float values Example: 1.
     """

    cable_length: int
    cable_loss_per_hundred_ft: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cable_length = self.cable_length

        cable_loss_per_hundred_ft = self.cable_loss_per_hundred_ft


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cableLength": cable_length,
            "cableLossPerHundredFt": cable_loss_per_hundred_ft,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cable_length = d.pop("cableLength")

        cable_loss_per_hundred_ft = d.pop("cableLossPerHundredFt")

        each_read_point = cls(
            cable_length=cable_length,
            cable_loss_per_hundred_ft=cable_loss_per_hundred_ft,
        )


        each_read_point.additional_properties = d
        return each_read_point

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
