from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.memory_stats import MemoryStats





T = TypeVar("T", bound="ReaderFlashMemory")



@_attrs_define
class ReaderFlashMemory:
    """ Non-volatile reader flash partitions and their usage information

        Attributes:
            root_file_system (MemoryStats): System memory statistics
            platform (MemoryStats): System memory statistics
            reader_config (MemoryStats): System memory statistics
            reader_data (MemoryStats): System memory statistics
     """

    root_file_system: 'MemoryStats'
    platform: 'MemoryStats'
    reader_config: 'MemoryStats'
    reader_data: 'MemoryStats'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.memory_stats import MemoryStats
        root_file_system = self.root_file_system.to_dict()

        platform = self.platform.to_dict()

        reader_config = self.reader_config.to_dict()

        reader_data = self.reader_data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "rootFileSystem": root_file_system,
            "platform": platform,
            "readerConfig": reader_config,
            "readerData": reader_data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.memory_stats import MemoryStats
        d = dict(src_dict)
        root_file_system = MemoryStats.from_dict(d.pop("rootFileSystem"))




        platform = MemoryStats.from_dict(d.pop("platform"))




        reader_config = MemoryStats.from_dict(d.pop("readerConfig"))




        reader_data = MemoryStats.from_dict(d.pop("readerData"))




        reader_flash_memory = cls(
            root_file_system=root_file_system,
            platform=platform,
            reader_config=reader_config,
            reader_data=reader_data,
        )


        reader_flash_memory.additional_properties = d
        return reader_flash_memory

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
