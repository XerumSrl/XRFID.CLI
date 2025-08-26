from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.set_install_userapp_body_authentication_type import check_set_install_userapp_body_authentication_type
from ..models.set_install_userapp_body_authentication_type import SetInstallUserappBodyAuthenticationType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.set_install_userapp_body_options import SetInstallUserappBodyOptions





T = TypeVar("T", bound="SetInstallUserappBody")



@_attrs_define
class SetInstallUserappBody:
    """ 
        Attributes:
            url (str): http or https file server url Example: https://example.com/apps/.
            filename (str): userapp filename in file server Example: sample_1.0.0.deb.
            authentication_type (SetInstallUserappBodyAuthenticationType): file server authentication type Example: NONE.
            options (Union[Unset, SetInstallUserappBodyOptions]): file server basic authentication options
            verify_peer (Union[Unset, bool]): verify file server certificate Default: True.
            verify_host (Union[Unset, bool]): verify file server hostname Default: True.
            ca_certificate_file_location (Union[Unset, str]): CA file location to be used for server authentication Example:
                /apps/ca.pem.
            ca_certificate_file_content (Union[Unset, str]): CA certificate file content to be used for server
                authentication
     """

    url: str
    filename: str
    authentication_type: SetInstallUserappBodyAuthenticationType
    options: Union[Unset, 'SetInstallUserappBodyOptions'] = UNSET
    verify_peer: Union[Unset, bool] = True
    verify_host: Union[Unset, bool] = True
    ca_certificate_file_location: Union[Unset, str] = UNSET
    ca_certificate_file_content: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.set_install_userapp_body_options import SetInstallUserappBodyOptions
        url = self.url

        filename = self.filename

        authentication_type: str = self.authentication_type

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        verify_peer = self.verify_peer

        verify_host = self.verify_host

        ca_certificate_file_location = self.ca_certificate_file_location

        ca_certificate_file_content = self.ca_certificate_file_content


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "url": url,
            "filename": filename,
            "authenticationType": authentication_type,
        })
        if options is not UNSET:
            field_dict["options"] = options
        if verify_peer is not UNSET:
            field_dict["verifyPeer"] = verify_peer
        if verify_host is not UNSET:
            field_dict["verifyHost"] = verify_host
        if ca_certificate_file_location is not UNSET:
            field_dict["CACertificateFileLocation"] = ca_certificate_file_location
        if ca_certificate_file_content is not UNSET:
            field_dict["CACertificateFileContent"] = ca_certificate_file_content

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_install_userapp_body_options import SetInstallUserappBodyOptions
        d = dict(src_dict)
        url = d.pop("url")

        filename = d.pop("filename")

        authentication_type = check_set_install_userapp_body_authentication_type(d.pop("authenticationType"))




        _options = d.pop("options", UNSET)
        options: Union[Unset, SetInstallUserappBodyOptions]
        if isinstance(_options,  Unset):
            options = UNSET
        else:
            options = SetInstallUserappBodyOptions.from_dict(_options)




        verify_peer = d.pop("verifyPeer", UNSET)

        verify_host = d.pop("verifyHost", UNSET)

        ca_certificate_file_location = d.pop("CACertificateFileLocation", UNSET)

        ca_certificate_file_content = d.pop("CACertificateFileContent", UNSET)

        set_install_userapp_body = cls(
            url=url,
            filename=filename,
            authentication_type=authentication_type,
            options=options,
            verify_peer=verify_peer,
            verify_host=verify_host,
            ca_certificate_file_location=ca_certificate_file_location,
            ca_certificate_file_content=ca_certificate_file_content,
        )


        set_install_userapp_body.additional_properties = d
        return set_install_userapp_body

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
