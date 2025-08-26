from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="TCPIPSecurity")



@_attrs_define
class TCPIPSecurity:
    """ Configuration of TCPIP Security

        Attributes:
            verify_peer (bool): Enables or Disabled verifying that the server cert is for the server to which the message is
                being posted
            ca_certificate_file_location (str): Path and file name of the CA Certificate
            installed_certificate_name (str): Name of certificate installed on the reader
            installed_certificate_type (str): Type of certificate installed on the reader
            use_local_certs (bool): Enable or Disable use of local certificates
     """

    verify_peer: bool
    ca_certificate_file_location: str
    installed_certificate_name: str
    installed_certificate_type: str
    use_local_certs: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        verify_peer = self.verify_peer

        ca_certificate_file_location = self.ca_certificate_file_location

        installed_certificate_name = self.installed_certificate_name

        installed_certificate_type = self.installed_certificate_type

        use_local_certs = self.use_local_certs


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "verifyPeer": verify_peer,
            "CACertificateFileLocation": ca_certificate_file_location,
            "installedCertificateName": installed_certificate_name,
            "installedCertificateType": installed_certificate_type,
            "useLocalCerts": use_local_certs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        verify_peer = d.pop("verifyPeer")

        ca_certificate_file_location = d.pop("CACertificateFileLocation")

        installed_certificate_name = d.pop("installedCertificateName")

        installed_certificate_type = d.pop("installedCertificateType")

        use_local_certs = d.pop("useLocalCerts")

        tcpip_security = cls(
            verify_peer=verify_peer,
            ca_certificate_file_location=ca_certificate_file_location,
            installed_certificate_name=installed_certificate_name,
            installed_certificate_type=installed_certificate_type,
            use_local_certs=use_local_certs,
        )


        tcpip_security.additional_properties = d
        return tcpip_security

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
