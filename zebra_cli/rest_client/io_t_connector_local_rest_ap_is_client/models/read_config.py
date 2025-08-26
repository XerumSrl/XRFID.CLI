from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.read_config_membank import check_read_config_membank
from ..models.read_config_membank import ReadConfigMembank
from typing import cast






T = TypeVar("T", bound="ReadConfig")



@_attrs_define
class ReadConfig:
    """ 
        Attributes:
            membank (ReadConfigMembank): Membank Field (see EPC Gen2 Spec)
            word_pointer (int): WordPtr Field (see EPC Gen2 Spec)
            word_counter (int): WordPtr Field (see EPC Gen2 Spec)
     """

    membank: ReadConfigMembank
    word_pointer: int
    word_counter: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        membank: str = self.membank

        word_pointer = self.word_pointer

        word_counter = self.word_counter


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "membank": membank,
            "wordPointer": word_pointer,
            "wordCounter": word_counter,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        membank = check_read_config_membank(d.pop("membank"))




        word_pointer = d.pop("wordPointer")

        word_counter = d.pop("wordCounter")

        read_config = cls(
            membank=membank,
            word_pointer=word_pointer,
            word_counter=word_counter,
        )


        read_config.additional_properties = d
        return read_config

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
