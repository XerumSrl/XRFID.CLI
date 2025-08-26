from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ReaderNetwork")



@_attrs_define
class ReaderNetwork:
    """ Reader network information

        Attributes:
            host_name (str): Host name of the reader Example: FX9600F0F4B5.
            ip_address (str): IP address of the reader Example: 192.168.1.10.
            gateway_address (str): IP address of the gateway Example: 192.168.1.1.
            subnet_mask (str): Subnet mask for the network adapter Example: 255.255.255.0.
            dns_address (str): IP address of the DNS server Example: 8.8.8.8.
            dhcp (bool): A value indicating DHCP configuration Example: true.
            mac_address (str): MAC address of the reader Example: 84:24:8D:F0:F4:B5.
     """

    host_name: str
    ip_address: str
    gateway_address: str
    subnet_mask: str
    dns_address: str
    dhcp: bool
    mac_address: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        host_name = self.host_name

        ip_address = self.ip_address

        gateway_address = self.gateway_address

        subnet_mask = self.subnet_mask

        dns_address = self.dns_address

        dhcp = self.dhcp

        mac_address = self.mac_address


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "hostName": host_name,
            "ipAddress": ip_address,
            "gatewayAddress": gateway_address,
            "subnetMask": subnet_mask,
            "dnsAddress": dns_address,
            "dhcp": dhcp,
            "macAddress": mac_address,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        host_name = d.pop("hostName")

        ip_address = d.pop("ipAddress")

        gateway_address = d.pop("gatewayAddress")

        subnet_mask = d.pop("subnetMask")

        dns_address = d.pop("dnsAddress")

        dhcp = d.pop("dhcp")

        mac_address = d.pop("macAddress")

        reader_network = cls(
            host_name=host_name,
            ip_address=ip_address,
            gateway_address=gateway_address,
            subnet_mask=subnet_mask,
            dns_address=dns_address,
            dhcp=dhcp,
            mac_address=mac_address,
        )


        reader_network.additional_properties = d
        return reader_network

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
