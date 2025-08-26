from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.kill_type import check_kill_type
from ..models.kill_type import KillType
from typing import cast

if TYPE_CHECKING:
  from ..models.kill_config import KillConfig





T = TypeVar("T", bound="Kill")



@_attrs_define
class Kill:
    """ 
        Attributes:
            type_ (KillType):
            config (KillConfig):
     """

    type_: KillType
    config: 'KillConfig'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.kill_config import KillConfig
        type_: str = self.type_

        config = self.config.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "config": config,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.kill_config import KillConfig
        d = dict(src_dict)
        type_ = check_kill_type(d.pop("type"))




        config = KillConfig.from_dict(d.pop("config"))




        kill = cls(
            type_=type_,
            config=config,
        )


        kill.additional_properties = d
        return kill

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
