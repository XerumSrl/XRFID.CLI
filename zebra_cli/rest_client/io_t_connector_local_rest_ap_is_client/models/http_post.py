from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.http_post_security import HTTPPostSecurity





T = TypeVar("T", bound="HTTPPost")



@_attrs_define
class HTTPPost:
    """ Configuration of HTTP Post

        Attributes:
            url (str): Destination URL to Post messages
            security (HTTPPostSecurity): Configuration of HTTP Post Security
     """

    url: str
    security: 'HTTPPostSecurity'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.http_post_security import HTTPPostSecurity
        url = self.url

        security = self.security.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "URL": url,
            "security": security,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_post_security import HTTPPostSecurity
        d = dict(src_dict)
        url = d.pop("URL")

        security = HTTPPostSecurity.from_dict(d.pop("security"))




        http_post = cls(
            url=url,
            security=security,
        )


        http_post.additional_properties = d
        return http_post

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
