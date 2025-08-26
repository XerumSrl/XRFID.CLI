from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_certificates_response_200_type import check_get_certificates_response_200_type
from ..models.get_certificates_response_200_type import GetCertificatesResponse200Type
from typing import cast






T = TypeVar("T", bound="GetCertificatesResponse200")



@_attrs_define
class GetCertificatesResponse200:
    """ 
        Attributes:
            name (str): certificate name Example: Reader Main Certificates.
            type_ (GetCertificatesResponse200Type): certificate type Example: server.
            install_time (str): certificate installation time Example: Mon Jun 21 12:38:03 2021.
            issuer_name (str): Certificate issuer name Example: FX9600EE5729.
            publickey (str): public key content
            serial (str): certificate serial Example: 410835777.
            subject_name (str): certificate subject name
            validity_start (str): certificate validity start date (DD/MM/YYYY) Example: 21/06/2021.
            validity_end (str): certificate validity end date (DD/MM/YYYY) Example: 16/06/2041.
     """

    name: str
    type_: GetCertificatesResponse200Type
    install_time: str
    issuer_name: str
    publickey: str
    serial: str
    subject_name: str
    validity_start: str
    validity_end: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_: str = self.type_

        install_time = self.install_time

        issuer_name = self.issuer_name

        publickey = self.publickey

        serial = self.serial

        subject_name = self.subject_name

        validity_start = self.validity_start

        validity_end = self.validity_end


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "type": type_,
            "installTime": install_time,
            "issuerName": issuer_name,
            "publickey": publickey,
            "serial": serial,
            "subjectName": subject_name,
            "validityStart": validity_start,
            "validityEnd": validity_end,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = check_get_certificates_response_200_type(d.pop("type"))




        install_time = d.pop("installTime")

        issuer_name = d.pop("issuerName")

        publickey = d.pop("publickey")

        serial = d.pop("serial")

        subject_name = d.pop("subjectName")

        validity_start = d.pop("validityStart")

        validity_end = d.pop("validityEnd")

        get_certificates_response_200 = cls(
            name=name,
            type_=type_,
            install_time=install_time,
            issuer_name=issuer_name,
            publickey=publickey,
            serial=serial,
            subject_name=subject_name,
            validity_start=validity_start,
            validity_end=validity_end,
        )


        get_certificates_response_200.additional_properties = d
        return get_certificates_response_200

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
