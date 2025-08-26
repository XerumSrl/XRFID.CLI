from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="HTTPPostTLSAuthentication")



@_attrs_define
class HTTPPostTLSAuthentication:
    """ HTTP Server TLS certificates details

        Attributes:
            public_key_file_location (str): Path and file name of the Public Key
            private_key_file_location (str): Path and file name of the Private Key
     """

    public_key_file_location: str
    private_key_file_location: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        public_key_file_location = self.public_key_file_location

        private_key_file_location = self.private_key_file_location


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "publicKeyFileLocation": public_key_file_location,
            "privateKeyFileLocation": private_key_file_location,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        public_key_file_location = d.pop("publicKeyFileLocation")

        private_key_file_location = d.pop("privateKeyFileLocation")

        http_post_tls_authentication = cls(
            public_key_file_location=public_key_file_location,
            private_key_file_location=private_key_file_location,
        )


        http_post_tls_authentication.additional_properties = d
        return http_post_tls_authentication

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
