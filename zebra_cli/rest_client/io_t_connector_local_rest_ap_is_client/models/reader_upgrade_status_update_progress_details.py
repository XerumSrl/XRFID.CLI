from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="ReaderUpgradeStatusUpdateProgressDetails")



@_attrs_define
class ReaderUpgradeStatusUpdateProgressDetails:
    """ 
        Attributes:
            os (Union[Unset, float]): OS upgrade progress percentage
            root_file_system (Union[Unset, float]): Root file system upgrade progress percentage
            applications (Union[Unset, float]): Applications upgrade progress percentage
            radio_firmware (Union[Unset, float]): Radio firmware upgrade progress percentage
            platform (Union[Unset, float]): Platform upgrade progress percentage
     """

    os: Union[Unset, float] = UNSET
    root_file_system: Union[Unset, float] = UNSET
    applications: Union[Unset, float] = UNSET
    radio_firmware: Union[Unset, float] = UNSET
    platform: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        os = self.os

        root_file_system = self.root_file_system

        applications = self.applications

        radio_firmware = self.radio_firmware

        platform = self.platform


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if os is not UNSET:
            field_dict["os"] = os
        if root_file_system is not UNSET:
            field_dict["rootFileSystem"] = root_file_system
        if applications is not UNSET:
            field_dict["applications"] = applications
        if radio_firmware is not UNSET:
            field_dict["radioFirmware"] = radio_firmware
        if platform is not UNSET:
            field_dict["platform"] = platform

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        os = d.pop("os", UNSET)

        root_file_system = d.pop("rootFileSystem", UNSET)

        applications = d.pop("applications", UNSET)

        radio_firmware = d.pop("radioFirmware", UNSET)

        platform = d.pop("platform", UNSET)

        reader_upgrade_status_update_progress_details = cls(
            os=os,
            root_file_system=root_file_system,
            applications=applications,
            radio_firmware=radio_firmware,
            platform=platform,
        )


        reader_upgrade_status_update_progress_details.additional_properties = d
        return reader_upgrade_status_update_progress_details

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
