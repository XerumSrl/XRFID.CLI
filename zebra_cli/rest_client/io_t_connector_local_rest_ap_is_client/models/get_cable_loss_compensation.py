from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.get_cable_loss_compensation_read_point import GetCableLossCompensationReadPoint





T = TypeVar("T", bound="GetCableLossCompensation")



@_attrs_define
class GetCableLossCompensation:
    """ Gets the Reader Cable Loss Compensation. Includes Cable Length and Cable Loss per Hundred Feet

        Attributes:
            read_point (GetCableLossCompensationReadPoint): Returns cable loss compensation per read point labeled 1,2,3...
                upto max supported read points
     """

    read_point: 'GetCableLossCompensationReadPoint'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_cable_loss_compensation_read_point import GetCableLossCompensationReadPoint
        read_point = self.read_point.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "<readPoint>": read_point,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_cable_loss_compensation_read_point import GetCableLossCompensationReadPoint
        d = dict(src_dict)
        read_point = GetCableLossCompensationReadPoint.from_dict(d.pop("<readPoint>"))




        get_cable_loss_compensation = cls(
            read_point=read_point,
        )


        get_cable_loss_compensation.additional_properties = d
        return get_cable_loss_compensation

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
