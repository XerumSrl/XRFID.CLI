from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.get_reader_capabilites_capabilities import GetReaderCapabilitesCapabilities





T = TypeVar("T", bound="GetReaderCapabilites")



@_attrs_define
class GetReaderCapabilites:
    """ Defines the capabilities present on the reader

        Attributes:
            capabilities (GetReaderCapabilitesCapabilities):
     """

    capabilities: 'GetReaderCapabilitesCapabilities'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_reader_capabilites_capabilities import GetReaderCapabilitesCapabilities
        capabilities = self.capabilities.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "capabilities": capabilities,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_reader_capabilites_capabilities import GetReaderCapabilitesCapabilities
        d = dict(src_dict)
        capabilities = GetReaderCapabilitesCapabilities.from_dict(d.pop("capabilities"))




        get_reader_capabilites = cls(
            capabilities=capabilities,
        )


        get_reader_capabilites.additional_properties = d
        return get_reader_capabilites

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
