from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.write_config_membank import check_write_config_membank
from ..models.write_config_membank import WriteConfigMembank
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="WriteConfig")



@_attrs_define
class WriteConfig:
    """ 
        Attributes:
            membank (WriteConfigMembank): Membank Field (see EPC Gen2 Spec)
            word_pointer (int): WordPtr Field (see EPC Gen2 Spec)
            data (str): Data Field (see EPC Gen2 Spec) Hex string indicating the word(s) to be written. Unlike the Gen2
                Spec, the length of the data field can be more than a single 16 bit word. However, the length of the string must
                be a multiple of 16 bit words Example: 11112222.
            block_size (Union[Unset, int]): Block size - if set to non-zero value, the reader will use the BlockWrite
                command set write the data (and not the simple Write command). The value indicates the number of 16-bit words to
                use for each block
     """

    membank: WriteConfigMembank
    word_pointer: int
    data: str
    block_size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        membank: str = self.membank

        word_pointer = self.word_pointer

        data = self.data

        block_size = self.block_size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "membank": membank,
            "wordPointer": word_pointer,
            "data": data,
        })
        if block_size is not UNSET:
            field_dict["blockSize"] = block_size

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        membank = check_write_config_membank(d.pop("membank"))




        word_pointer = d.pop("wordPointer")

        data = d.pop("data")

        block_size = d.pop("blockSize", UNSET)

        write_config = cls(
            membank=membank,
            word_pointer=word_pointer,
            data=data,
            block_size=block_size,
        )


        write_config.additional_properties = d
        return write_config

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
