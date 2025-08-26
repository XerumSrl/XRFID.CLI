from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="AZUREEndpoint")



@_attrs_define
class AZUREEndpoint:
    """ Enable or Disable Security

        Attributes:
            hostname (Union[Unset, str]): Server hostname
            protocol (Union[Unset, str]): Connection protocol
            port (Union[Unset, int]): Connection port
     """

    hostname: Union[Unset, str] = UNSET
    protocol: Union[Unset, str] = UNSET
    port: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        hostname = self.hostname

        protocol = self.protocol

        port = self.port


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if hostname is not UNSET:
            field_dict["hostname"] = hostname
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if port is not UNSET:
            field_dict["port"] = port

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hostname = d.pop("hostname", UNSET)

        protocol = d.pop("protocol", UNSET)

        port = d.pop("port", UNSET)

        azure_endpoint = cls(
            hostname=hostname,
            protocol=protocol,
            port=port,
        )


        azure_endpoint.additional_properties = d
        return azure_endpoint

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
