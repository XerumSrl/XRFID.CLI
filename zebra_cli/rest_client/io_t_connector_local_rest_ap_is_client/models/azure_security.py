from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="AZURESecurity")



@_attrs_define
class AZURESecurity:
    """ 
        Attributes:
            key_formant (Union[Unset, str]): Key Format
            key_algorithm (Union[Unset, str]): Key Algorithm used
            ca_certificate_file_location (Union[Unset, str]): Path to CA Certificate location
            public_key_file_location (Union[Unset, str]): Path to public key file
            private_key_file_location (Union[Unset, str]): Path to private key file
            verify_host_name (Union[Unset, bool]): Enable or Disable host name verification
            verify_peer (Union[Unset, bool]): Enable or Disable peer verification
     """

    key_formant: Union[Unset, str] = UNSET
    key_algorithm: Union[Unset, str] = UNSET
    ca_certificate_file_location: Union[Unset, str] = UNSET
    public_key_file_location: Union[Unset, str] = UNSET
    private_key_file_location: Union[Unset, str] = UNSET
    verify_host_name: Union[Unset, bool] = UNSET
    verify_peer: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        key_formant = self.key_formant

        key_algorithm = self.key_algorithm

        ca_certificate_file_location = self.ca_certificate_file_location

        public_key_file_location = self.public_key_file_location

        private_key_file_location = self.private_key_file_location

        verify_host_name = self.verify_host_name

        verify_peer = self.verify_peer


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if key_formant is not UNSET:
            field_dict["keyFormant"] = key_formant
        if key_algorithm is not UNSET:
            field_dict["keyAlgorithm"] = key_algorithm
        if ca_certificate_file_location is not UNSET:
            field_dict["CACertificateFileLocation"] = ca_certificate_file_location
        if public_key_file_location is not UNSET:
            field_dict["publicKeyFileLocation"] = public_key_file_location
        if private_key_file_location is not UNSET:
            field_dict["privateKeyFileLocation"] = private_key_file_location
        if verify_host_name is not UNSET:
            field_dict["verifyHostName"] = verify_host_name
        if verify_peer is not UNSET:
            field_dict["verifyPeer"] = verify_peer

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_formant = d.pop("keyFormant", UNSET)

        key_algorithm = d.pop("keyAlgorithm", UNSET)

        ca_certificate_file_location = d.pop("CACertificateFileLocation", UNSET)

        public_key_file_location = d.pop("publicKeyFileLocation", UNSET)

        private_key_file_location = d.pop("privateKeyFileLocation", UNSET)

        verify_host_name = d.pop("verifyHostName", UNSET)

        verify_peer = d.pop("verifyPeer", UNSET)

        azure_security = cls(
            key_formant=key_formant,
            key_algorithm=key_algorithm,
            ca_certificate_file_location=ca_certificate_file_location,
            public_key_file_location=public_key_file_location,
            private_key_file_location=private_key_file_location,
            verify_host_name=verify_host_name,
            verify_peer=verify_peer,
        )


        azure_security.additional_properties = d
        return azure_security

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
