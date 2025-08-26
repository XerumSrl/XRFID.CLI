from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lock_type import check_lock_type
from ..models.lock_type import LockType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.lock_config import LockConfig





T = TypeVar("T", bound="Lock")



@_attrs_define
class Lock:
    """ 
        Attributes:
            config (LockConfig):
            type_ (Union[Unset, LockType]):
     """

    config: 'LockConfig'
    type_: Union[Unset, LockType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lock_config import LockConfig
        config = self.config.to_dict()

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "config": config,
        })
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lock_config import LockConfig
        d = dict(src_dict)
        config = LockConfig.from_dict(d.pop("config"))




        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, LockType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = check_lock_type(_type_)




        lock = cls(
            config=config,
            type_=type_,
        )


        lock.additional_properties = d
        return lock

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
