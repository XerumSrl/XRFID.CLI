from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ReaderVersionRevertBackFirmware")



@_attrs_define
class ReaderVersionRevertBackFirmware:
    """ current revertback firmware details

        Attributes:
            reader_application (str): revertback firmware version Example: 3.25.60.0.
            reader_boot_loader (str): revertback boot loader version Example: 3.17.6.0.
            reader_file_system (str): revertback file system version Example: 3.21.8.0.
            reader_os (str): revertback os version Example: 3.20.2.0.
     """

    reader_application: str
    reader_boot_loader: str
    reader_file_system: str
    reader_os: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        reader_application = self.reader_application

        reader_boot_loader = self.reader_boot_loader

        reader_file_system = self.reader_file_system

        reader_os = self.reader_os


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "readerApplication": reader_application,
            "readerBootLoader": reader_boot_loader,
            "readerFileSystem": reader_file_system,
            "readerOS": reader_os,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reader_application = d.pop("readerApplication")

        reader_boot_loader = d.pop("readerBootLoader")

        reader_file_system = d.pop("readerFileSystem")

        reader_os = d.pop("readerOS")

        reader_version_revert_back_firmware = cls(
            reader_application=reader_application,
            reader_boot_loader=reader_boot_loader,
            reader_file_system=reader_file_system,
            reader_os=reader_os,
        )


        reader_version_revert_back_firmware.additional_properties = d
        return reader_version_revert_back_firmware

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
