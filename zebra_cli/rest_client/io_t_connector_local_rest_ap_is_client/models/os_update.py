from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.os_update_authentication_type import check_os_update_authentication_type
from ..models.os_update_authentication_type import OsUpdateAuthenticationType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.os_update_options import OsUpdateOptions





T = TypeVar("T", bound="OsUpdate")



@_attrs_define
class OsUpdate:
    """ 
        Attributes:
            url (str): URL where the OS image is served Example: http://169.254.149.144:8000/firmware.
            authentication_type (OsUpdateAuthenticationType): Type of authentication required to get OS image
            options (Union[Unset, OsUpdateOptions]):
     """

    url: str
    authentication_type: OsUpdateAuthenticationType
    options: Union[Unset, 'OsUpdateOptions'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.os_update_options import OsUpdateOptions
        url = self.url

        authentication_type: str = self.authentication_type

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "url": url,
            "authenticationType": authentication_type,
        })
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.os_update_options import OsUpdateOptions
        d = dict(src_dict)
        url = d.pop("url")

        authentication_type = check_os_update_authentication_type(d.pop("authenticationType"))




        _options = d.pop("options", UNSET)
        options: Union[Unset, OsUpdateOptions]
        if isinstance(_options,  Unset):
            options = UNSET
        else:
            options = OsUpdateOptions.from_dict(_options)




        os_update = cls(
            url=url,
            authentication_type=authentication_type,
            options=options,
        )


        os_update.additional_properties = d
        return os_update

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
