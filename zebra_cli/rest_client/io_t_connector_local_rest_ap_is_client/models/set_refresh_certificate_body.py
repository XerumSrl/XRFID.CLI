from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.set_refresh_certificate_body_type import check_set_refresh_certificate_body_type
from ..models.set_refresh_certificate_body_type import SetRefreshCertificateBodyType
from typing import cast






T = TypeVar("T", bound="SetRefreshCertificateBody")



@_attrs_define
class SetRefreshCertificateBody:
    """ 
        Attributes:
            type_ (SetRefreshCertificateBodyType): certificate type Example: app.
     """

    type_: SetRefreshCertificateBodyType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_set_refresh_certificate_body_type(d.pop("type"))




        set_refresh_certificate_body = cls(
            type_=type_,
        )


        set_refresh_certificate_body.additional_properties = d
        return set_refresh_certificate_body

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
