from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_reader_capabilites_capabilities_antennas_item_type import check_get_reader_capabilites_capabilities_antennas_item_type
from ..models.get_reader_capabilites_capabilities_antennas_item_type import GetReaderCapabilitesCapabilitiesAntennasItemType
from typing import cast






T = TypeVar("T", bound="GetReaderCapabilitesCapabilitiesAntennasItem")



@_attrs_define
class GetReaderCapabilitesCapabilitiesAntennasItem:
    """ port and type of port for each antenna

        Attributes:
            port (int): Port Number Example: 1.
            type_ (GetReaderCapabilitesCapabilitiesAntennasItemType): Type of port
     """

    port: int
    type_: GetReaderCapabilitesCapabilitiesAntennasItemType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        port = self.port

        type_: str = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "port": port,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        port = d.pop("port")

        type_ = check_get_reader_capabilites_capabilities_antennas_item_type(d.pop("type"))




        get_reader_capabilites_capabilities_antennas_item = cls(
            port=port,
            type_=type_,
        )


        get_reader_capabilites_capabilities_antennas_item.additional_properties = d
        return get_reader_capabilites_capabilities_antennas_item

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
