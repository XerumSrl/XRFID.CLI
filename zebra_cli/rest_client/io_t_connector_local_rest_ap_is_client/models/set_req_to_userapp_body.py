from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SetReqToUserappBody")



@_attrs_define
class SetReqToUserappBody:
    """ 
        Attributes:
            userapp (str): name of userapp to send command Example: sample.
            command (str): custom command or data to send
     """

    userapp: str
    command: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        userapp = self.userapp

        command = self.command


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "userapp": userapp,
            "command": command,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        userapp = d.pop("userapp")

        command = d.pop("command")

        set_req_to_userapp_body = cls(
            userapp=userapp,
            command=command,
        )


        set_req_to_userapp_body.additional_properties = d
        return set_req_to_userapp_body

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
