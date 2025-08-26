from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="GetUserappsResponse200Item")



@_attrs_define
class GetUserappsResponse200Item:
    """ 
        Attributes:
            appname (str): userapp name Example: sample.
            autostart (bool): autostart setting
            metadata (str): userapp metadata
            running_status (bool): userapp running status
     """

    appname: str
    autostart: bool
    metadata: str
    running_status: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        appname = self.appname

        autostart = self.autostart

        metadata = self.metadata

        running_status = self.running_status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "appname": appname,
            "autostart": autostart,
            "metadata": metadata,
            "runningStatus": running_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        appname = d.pop("appname")

        autostart = d.pop("autostart")

        metadata = d.pop("metadata")

        running_status = d.pop("runningStatus")

        get_userapps_response_200_item = cls(
            appname=appname,
            autostart=autostart,
            metadata=metadata,
            running_status=running_status,
        )


        get_userapps_response_200_item.additional_properties = d
        return get_userapps_response_200_item

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
