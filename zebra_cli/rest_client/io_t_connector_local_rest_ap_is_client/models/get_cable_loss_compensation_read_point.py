from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="GetCableLossCompensationReadPoint")



@_attrs_define
class GetCableLossCompensationReadPoint:
    """ Returns cable loss compensation per read point labeled 1,2,3... upto max supported read points

        Attributes:
            cable_length (int): Cable Length Field. Returns float values Example: 1.
            cable_loss_per_hundred_ft (int): Cable Loss per Hundred Feet. Returns float values Example: 1.
     """

    cable_length: int
    cable_loss_per_hundred_ft: int





    def to_dict(self) -> dict[str, Any]:
        cable_length = self.cable_length

        cable_loss_per_hundred_ft = self.cable_loss_per_hundred_ft


        field_dict: dict[str, Any] = {}

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

        get_cable_loss_compensation_read_point = cls(
            cable_length=cable_length,
            cable_loss_per_hundred_ft=cable_loss_per_hundred_ft,
        )

        return get_cable_loss_compensation_read_point

