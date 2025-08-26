from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.tcpip_security import TCPIPSecurity





T = TypeVar("T", bound="TCPIP")



@_attrs_define
class TCPIP:
    """ Configuration of TCPIP server

        Attributes:
            enable_security (bool): Enable or Disable Security
            security (TCPIPSecurity): Configuration of TCPIP Security
            tcpipport (str): TCPIP Connection port
     """

    enable_security: bool
    security: 'TCPIPSecurity'
    tcpipport: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.tcpip_security import TCPIPSecurity
        enable_security = self.enable_security

        security = self.security.to_dict()

        tcpipport = self.tcpipport


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "enableSecurity": enable_security,
            "security": security,
            "tcpipport": tcpipport,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tcpip_security import TCPIPSecurity
        d = dict(src_dict)
        enable_security = d.pop("enableSecurity")

        security = TCPIPSecurity.from_dict(d.pop("security"))




        tcpipport = d.pop("tcpipport")

        tcpip = cls(
            enable_security=enable_security,
            security=security,
            tcpipport=tcpipport,
        )


        tcpip.additional_properties = d
        return tcpip

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
