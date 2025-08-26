from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.set_update_certificate_authentication_type import check_set_update_certificate_authentication_type
from ..models.set_update_certificate_authentication_type import SetUpdateCertificateAuthenticationType
from ..models.set_update_certificate_type import check_set_update_certificate_type
from ..models.set_update_certificate_type import SetUpdateCertificateType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.set_update_certificate_headers import SetUpdateCertificateHeaders
  from ..models.set_update_certificate_options import SetUpdateCertificateOptions





T = TypeVar("T", bound="SetUpdateCertificate")



@_attrs_define
class SetUpdateCertificate:
    """ Install certificate

        Attributes:
            name (str): name of certificate Example: test.
            type_ (SetUpdateCertificateType): certificate type Example: client.
            url (str): ftps server url hosting certificate pfx file Example: ftps://10.17.231.92/CA-
                Certs_3.18.2/myCA/reader.pfx.
            authentication_type (Union[Unset, SetUpdateCertificateAuthenticationType]): ftps server authentication type
            pfx_file_name (Union[Unset, str]): PFX certiifcates file Name Example: dfbhnhf.
            pfx_content (Union[Unset, str]): pfx certificate content Example: mhmfgm.
            timeout_in_sec (Union[Unset, float]):
            filename (Union[Unset, str]): certificate file name
                 Example: czdsvfs.
            verify_host (Union[Unset, bool]): verify host boolean
            verify_peer (Union[Unset, bool]): verify peer boolean
            ca_certificate_file_location (Union[Unset, str]): CA Certification File Location Example: gfwwhg.
            ca_certificate_file_content (Union[Unset, str]): CA Certificate File Content Example: wehwe.
            installed_certificate_type (Union[Unset, str]): Installed Certificate Type
            installed_certificate_name (Union[Unset, str]): Installed Certificate Name
            public_key_file_location (Union[Unset, str]): public key file path
            public_key_file_content (Union[Unset, str]): public key file content
            private_key_file_location (Union[Unset, str]): private key file path
            private_key_file_content (Union[Unset, str]): private key file content
            headers (Union[Unset, SetUpdateCertificateHeaders]):
            options (Union[Unset, SetUpdateCertificateOptions]):
     """

    name: str
    type_: SetUpdateCertificateType
    url: str
    authentication_type: Union[Unset, SetUpdateCertificateAuthenticationType] = UNSET
    pfx_file_name: Union[Unset, str] = UNSET
    pfx_content: Union[Unset, str] = UNSET
    timeout_in_sec: Union[Unset, float] = UNSET
    filename: Union[Unset, str] = UNSET
    verify_host: Union[Unset, bool] = UNSET
    verify_peer: Union[Unset, bool] = UNSET
    ca_certificate_file_location: Union[Unset, str] = UNSET
    ca_certificate_file_content: Union[Unset, str] = UNSET
    installed_certificate_type: Union[Unset, str] = UNSET
    installed_certificate_name: Union[Unset, str] = UNSET
    public_key_file_location: Union[Unset, str] = UNSET
    public_key_file_content: Union[Unset, str] = UNSET
    private_key_file_location: Union[Unset, str] = UNSET
    private_key_file_content: Union[Unset, str] = UNSET
    headers: Union[Unset, 'SetUpdateCertificateHeaders'] = UNSET
    options: Union[Unset, 'SetUpdateCertificateOptions'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.set_update_certificate_headers import SetUpdateCertificateHeaders
        from ..models.set_update_certificate_options import SetUpdateCertificateOptions
        name = self.name

        type_: str = self.type_

        url = self.url

        authentication_type: Union[Unset, str] = UNSET
        if not isinstance(self.authentication_type, Unset):
            authentication_type = self.authentication_type


        pfx_file_name = self.pfx_file_name

        pfx_content = self.pfx_content

        timeout_in_sec = self.timeout_in_sec

        filename = self.filename

        verify_host = self.verify_host

        verify_peer = self.verify_peer

        ca_certificate_file_location = self.ca_certificate_file_location

        ca_certificate_file_content = self.ca_certificate_file_content

        installed_certificate_type = self.installed_certificate_type

        installed_certificate_name = self.installed_certificate_name

        public_key_file_location = self.public_key_file_location

        public_key_file_content = self.public_key_file_content

        private_key_file_location = self.private_key_file_location

        private_key_file_content = self.private_key_file_content

        headers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "type": type_,
            "url": url,
        })
        if authentication_type is not UNSET:
            field_dict["authenticationType"] = authentication_type
        if pfx_file_name is not UNSET:
            field_dict["pfxFileName"] = pfx_file_name
        if pfx_content is not UNSET:
            field_dict["pfxContent"] = pfx_content
        if timeout_in_sec is not UNSET:
            field_dict["timeoutInSec"] = timeout_in_sec
        if filename is not UNSET:
            field_dict["filename"] = filename
        if verify_host is not UNSET:
            field_dict["verifyHost"] = verify_host
        if verify_peer is not UNSET:
            field_dict["verifyPeer"] = verify_peer
        if ca_certificate_file_location is not UNSET:
            field_dict["CACertificateFileLocation"] = ca_certificate_file_location
        if ca_certificate_file_content is not UNSET:
            field_dict["CACertificateFileContent"] = ca_certificate_file_content
        if installed_certificate_type is not UNSET:
            field_dict["installedCertificateType"] = installed_certificate_type
        if installed_certificate_name is not UNSET:
            field_dict["installedCertificateName"] = installed_certificate_name
        if public_key_file_location is not UNSET:
            field_dict["publicKeyFileLocation"] = public_key_file_location
        if public_key_file_content is not UNSET:
            field_dict["publicKeyFileContent"] = public_key_file_content
        if private_key_file_location is not UNSET:
            field_dict["privateKeyFileLocation"] = private_key_file_location
        if private_key_file_content is not UNSET:
            field_dict["privateKeyFileContent"] = private_key_file_content
        if headers is not UNSET:
            field_dict["headers"] = headers
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_update_certificate_headers import SetUpdateCertificateHeaders
        from ..models.set_update_certificate_options import SetUpdateCertificateOptions
        d = dict(src_dict)
        name = d.pop("name")

        type_ = check_set_update_certificate_type(d.pop("type"))




        url = d.pop("url")

        _authentication_type = d.pop("authenticationType", UNSET)
        authentication_type: Union[Unset, SetUpdateCertificateAuthenticationType]
        if isinstance(_authentication_type,  Unset):
            authentication_type = UNSET
        else:
            authentication_type = check_set_update_certificate_authentication_type(_authentication_type)




        pfx_file_name = d.pop("pfxFileName", UNSET)

        pfx_content = d.pop("pfxContent", UNSET)

        timeout_in_sec = d.pop("timeoutInSec", UNSET)

        filename = d.pop("filename", UNSET)

        verify_host = d.pop("verifyHost", UNSET)

        verify_peer = d.pop("verifyPeer", UNSET)

        ca_certificate_file_location = d.pop("CACertificateFileLocation", UNSET)

        ca_certificate_file_content = d.pop("CACertificateFileContent", UNSET)

        installed_certificate_type = d.pop("installedCertificateType", UNSET)

        installed_certificate_name = d.pop("installedCertificateName", UNSET)

        public_key_file_location = d.pop("publicKeyFileLocation", UNSET)

        public_key_file_content = d.pop("publicKeyFileContent", UNSET)

        private_key_file_location = d.pop("privateKeyFileLocation", UNSET)

        private_key_file_content = d.pop("privateKeyFileContent", UNSET)

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, SetUpdateCertificateHeaders]
        if isinstance(_headers,  Unset):
            headers = UNSET
        else:
            headers = SetUpdateCertificateHeaders.from_dict(_headers)




        _options = d.pop("options", UNSET)
        options: Union[Unset, SetUpdateCertificateOptions]
        if isinstance(_options,  Unset):
            options = UNSET
        else:
            options = SetUpdateCertificateOptions.from_dict(_options)




        set_update_certificate = cls(
            name=name,
            type_=type_,
            url=url,
            authentication_type=authentication_type,
            pfx_file_name=pfx_file_name,
            pfx_content=pfx_content,
            timeout_in_sec=timeout_in_sec,
            filename=filename,
            verify_host=verify_host,
            verify_peer=verify_peer,
            ca_certificate_file_location=ca_certificate_file_location,
            ca_certificate_file_content=ca_certificate_file_content,
            installed_certificate_type=installed_certificate_type,
            installed_certificate_name=installed_certificate_name,
            public_key_file_location=public_key_file_location,
            public_key_file_content=public_key_file_content,
            private_key_file_location=private_key_file_location,
            private_key_file_content=private_key_file_content,
            headers=headers,
            options=options,
        )


        set_update_certificate.additional_properties = d
        return set_update_certificate

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
