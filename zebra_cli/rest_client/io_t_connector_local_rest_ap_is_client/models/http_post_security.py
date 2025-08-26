from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.http_post_security_authentication_type import check_http_post_security_authentication_type
from ..models.http_post_security_authentication_type import HTTPPostSecurityAuthenticationType
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.http_post_basic_authentication import HTTPPostBasicAuthentication
  from ..models.http_post_tls_authentication import HTTPPostTLSAuthentication





T = TypeVar("T", bound="HTTPPostSecurity")



@_attrs_define
class HTTPPostSecurity:
    """ Configuration of HTTP Post Security

        Attributes:
            verify_peer (bool): Enables or Disabled verifying that the server cert is for the server to which the message is
                being posted
            verify_host (bool): Enable or Disable verifiying that host name in the certificate is valid for the host name to
                which messages are being posted
            authentication_type (HTTPPostSecurityAuthenticationType): Type of Authentication to use when posting message
            authentication_options (Union['HTTPPostBasicAuthentication', 'HTTPPostTLSAuthentication', Unset]): Configuration
                of the Authentication Options
            ca_certificate_file_location (Union[Unset, str]): Path and file name of the CA Certificate
     """

    verify_peer: bool
    verify_host: bool
    authentication_type: HTTPPostSecurityAuthenticationType
    authentication_options: Union['HTTPPostBasicAuthentication', 'HTTPPostTLSAuthentication', Unset] = UNSET
    ca_certificate_file_location: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.http_post_basic_authentication import HTTPPostBasicAuthentication
        from ..models.http_post_tls_authentication import HTTPPostTLSAuthentication
        verify_peer = self.verify_peer

        verify_host = self.verify_host

        authentication_type: str = self.authentication_type

        authentication_options: Union[Unset, dict[str, Any]]
        if isinstance(self.authentication_options, Unset):
            authentication_options = UNSET
        elif isinstance(self.authentication_options, HTTPPostBasicAuthentication):
            authentication_options = self.authentication_options.to_dict()
        else:
            authentication_options = self.authentication_options.to_dict()


        ca_certificate_file_location = self.ca_certificate_file_location


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "verifyPeer": verify_peer,
            "verifyHost": verify_host,
            "authenticationType": authentication_type,
        })
        if authentication_options is not UNSET:
            field_dict["authenticationOptions"] = authentication_options
        if ca_certificate_file_location is not UNSET:
            field_dict["CACertificateFileLocation"] = ca_certificate_file_location

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_post_basic_authentication import HTTPPostBasicAuthentication
        from ..models.http_post_tls_authentication import HTTPPostTLSAuthentication
        d = dict(src_dict)
        verify_peer = d.pop("verifyPeer")

        verify_host = d.pop("verifyHost")

        authentication_type = check_http_post_security_authentication_type(d.pop("authenticationType"))




        def _parse_authentication_options(data: object) -> Union['HTTPPostBasicAuthentication', 'HTTPPostTLSAuthentication', Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                authentication_options_type_0 = HTTPPostBasicAuthentication.from_dict(data)



                return authentication_options_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            authentication_options_type_1 = HTTPPostTLSAuthentication.from_dict(data)



            return authentication_options_type_1

        authentication_options = _parse_authentication_options(d.pop("authenticationOptions", UNSET))


        ca_certificate_file_location = d.pop("CACertificateFileLocation", UNSET)

        http_post_security = cls(
            verify_peer=verify_peer,
            verify_host=verify_host,
            authentication_type=authentication_type,
            authentication_options=authentication_options,
            ca_certificate_file_location=ca_certificate_file_location,
        )


        http_post_security.additional_properties = d
        return http_post_security

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
