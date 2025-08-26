from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.read_type import check_read_type
from ..models.read_type import ReadType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.read_config import ReadConfig





T = TypeVar("T", bound="Read")



@_attrs_define
class Read:
    """ 
        Attributes:
            type_ (ReadType):
            config (Union[Unset, ReadConfig]):
     """

    type_: ReadType
    config: Union[Unset, 'ReadConfig'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.read_config import ReadConfig
        type_: str = self.type_

        config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.read_config import ReadConfig
        d = dict(src_dict)
        type_ = check_read_type(d.pop("type"))




        _config = d.pop("config", UNSET)
        config: Union[Unset, ReadConfig]
        if isinstance(_config,  Unset):
            config = UNSET
        else:
            config = ReadConfig.from_dict(_config)




        read = cls(
            type_=type_,
            config=config,
        )


        read.additional_properties = d
        return read

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
