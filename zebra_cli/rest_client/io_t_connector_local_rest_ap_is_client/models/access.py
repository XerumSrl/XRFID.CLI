from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.access_type import AccessType
from ..models.access_type import check_access_type
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.access_config import AccessConfig





T = TypeVar("T", bound="Access")



@_attrs_define
class Access:
    """ 
        Attributes:
            type_ (Union[Unset, AccessType]):
            config (Union[Unset, AccessConfig]):
     """

    type_: Union[Unset, AccessType] = UNSET
    config: Union[Unset, 'AccessConfig'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.access_config import AccessConfig
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_


        config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_config import AccessConfig
        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AccessType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = check_access_type(_type_)




        _config = d.pop("config", UNSET)
        config: Union[Unset, AccessConfig]
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = AccessConfig.from_dict(_config)




        access = cls(
            type_=type_,
            config=config,
        )


        access.additional_properties = d
        return access

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
