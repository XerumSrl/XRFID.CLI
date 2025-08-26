from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="NetworkConfig")



@_attrs_define
class NetworkConfig:
    """ Represents reader communication configuration parameters.

        Attributes:
            dhcp (bool): A value indicating DHCP configuration Example: true.
            mac_adress (str): MAC address of the reader(read only) Example: 84:24:8D:F0:F4:B5.
            dns_address (str): IP address of the DNS server Example: 8.8.8.8.
            subnet_mask (str): Subnet mask for the network adapter Example: 255.255.255.0.
            gateway_address (str): IP address of the gateway Example: 192.168.1.1.
            ip_address (str): IP address of the reader (read only if dhcp = true) Example: 192.168.1.10.
            host_name (str): Hostname of the reader Example: FX9600F0F4B5.
     """

    dhcp: bool
    mac_adress: str
    dns_address: str
    subnet_mask: str
    gateway_address: str
    ip_address: str
    host_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        dhcp = self.dhcp

        mac_adress = self.mac_adress

        dns_address = self.dns_address

        subnet_mask = self.subnet_mask

        gateway_address = self.gateway_address

        ip_address = self.ip_address

        host_name = self.host_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "dhcp": dhcp,
            "macAdress": mac_adress,
            "dnsAddress": dns_address,
            "subnetMask": subnet_mask,
            "gatewayAddress": gateway_address,
            "ipAddress": ip_address,
            "hostName": host_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dhcp = d.pop("dhcp")

        mac_adress = d.pop("macAdress")

        dns_address = d.pop("dnsAddress")

        subnet_mask = d.pop("subnetMask")

        gateway_address = d.pop("gatewayAddress")

        ip_address = d.pop("ipAddress")

        host_name = d.pop("hostName")

        network_config = cls(
            dhcp=dhcp,
            mac_adress=mac_adress,
            dns_address=dns_address,
            subnet_mask=subnet_mask,
            gateway_address=gateway_address,
            ip_address=ip_address,
            host_name=host_name,
        )


        network_config.additional_properties = d
        return network_config

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
