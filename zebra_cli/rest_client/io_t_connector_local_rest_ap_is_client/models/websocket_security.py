from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="WebsocketSecurity")



@_attrs_define
class WebsocketSecurity:
    """ Configuration of Websocket Security

        Attributes:
            verify_peer (bool): Enables or Disabled verifying that the server cert is for the server to which the message is
                being posted
            verify_host (bool): Enable or Disable verifiying that host name in the certificate is valid for the host name to
                which messages are being posted
     """

    verify_peer: bool
    verify_host: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        verify_peer = self.verify_peer

        verify_host = self.verify_host


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "verifyPeer": verify_peer,
            "verifyHost": verify_host,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        verify_peer = d.pop("verifyPeer")

        verify_host = d.pop("verifyHost")

        websocket_security = cls(
            verify_peer=verify_peer,
            verify_host=verify_host,
        )


        websocket_security.additional_properties = d
        return websocket_security

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
