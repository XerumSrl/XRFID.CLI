from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.mqtt_security_key_algorithm import check_mqtt_security_key_algorithm
from ..models.mqtt_security_key_algorithm import MQTTSecurityKeyAlgorithm
from ..models.mqtt_security_key_format import check_mqtt_security_key_format
from ..models.mqtt_security_key_format import MQTTSecurityKeyFormat
from typing import cast






T = TypeVar("T", bound="MQTTSecurity")



@_attrs_define
class MQTTSecurity:
    """ Configuration of MQTT Security

        Attributes:
            key_format (MQTTSecurityKeyFormat): Format for the CA Certificate and Public and Private Keys
            key_algorithm (MQTTSecurityKeyAlgorithm): Algorithm used for the CA Certificate and Public and Private Keys
            ca_certificate_file_location (str): Path and file name of the CA Certificate
            public_key_file_location (str): Path and file name of the Public Key
            private_key_file_location (str): Path and file name of the Private Key
            verify_host_name (bool): check that the server certificate hostname matches the remote. Using this option means
                that you cannot be sure that the remote host is the server you wish to connect to and so is insecure.
     """

    key_format: MQTTSecurityKeyFormat
    key_algorithm: MQTTSecurityKeyAlgorithm
    ca_certificate_file_location: str
    public_key_file_location: str
    private_key_file_location: str
    verify_host_name: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        key_format: str = self.key_format

        key_algorithm: str = self.key_algorithm

        ca_certificate_file_location = self.ca_certificate_file_location

        public_key_file_location = self.public_key_file_location

        private_key_file_location = self.private_key_file_location

        verify_host_name = self.verify_host_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "keyFormat": key_format,
            "keyAlgorithm": key_algorithm,
            "CACertificateFileLocation": ca_certificate_file_location,
            "publicKeyFileLocation": public_key_file_location,
            "privateKeyFileLocation": private_key_file_location,
            "verifyHostName": verify_host_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key_format = check_mqtt_security_key_format(d.pop("keyFormat"))




        key_algorithm = check_mqtt_security_key_algorithm(d.pop("keyAlgorithm"))




        ca_certificate_file_location = d.pop("CACertificateFileLocation")

        public_key_file_location = d.pop("publicKeyFileLocation")

        private_key_file_location = d.pop("privateKeyFileLocation")

        verify_host_name = d.pop("verifyHostName")

        mqtt_security = cls(
            key_format=key_format,
            key_algorithm=key_algorithm,
            ca_certificate_file_location=ca_certificate_file_location,
            public_key_file_location=public_key_file_location,
            private_key_file_location=private_key_file_location,
            verify_host_name=verify_host_name,
        )


        mqtt_security.additional_properties = d
        return mqtt_security

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
