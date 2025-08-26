from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_reader_capabilites_capabilities_network_interfaces_item_ip_assignment_item import check_get_reader_capabilites_capabilities_network_interfaces_item_ip_assignment_item
from ..models.get_reader_capabilites_capabilities_network_interfaces_item_ip_assignment_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem
from ..models.get_reader_capabilites_capabilities_network_interfaces_item_ip_stack_item import check_get_reader_capabilites_capabilities_network_interfaces_item_ip_stack_item
from ..models.get_reader_capabilites_capabilities_network_interfaces_item_ip_stack_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem
from ..models.get_reader_capabilites_capabilities_network_interfaces_item_type import check_get_reader_capabilites_capabilities_network_interfaces_item_type
from ..models.get_reader_capabilites_capabilities_network_interfaces_item_type import GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType
from typing import cast






T = TypeVar("T", bound="GetReaderCapabilitesCapabilitiesNetworkInterfacesItem")



@_attrs_define
class GetReaderCapabilitesCapabilitiesNetworkInterfacesItem:
    """ 
        Attributes:
            802_1x (bool): Denotes if the reader supports IEEE 802.1x Standard
            internal (bool): Denotes if the network interface is internal or external
            ip_assignment (list[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem]): types of IP
                Assignments supported
            ip_stack (list[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem]): Denotes the type of IP stack
                supported by the interface
            type_ (GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType): Type of Network Interface
     """

    802_1x: bool
    internal: bool
    ip_assignment: list[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem]
    ip_stack: list[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem]
    type_: GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        802_1x = self.802_1x

        internal = self.internal

        ip_assignment = []
        for ip_assignment_item_data in self.ip_assignment:
            ip_assignment_item: str = ip_assignment_item_data
            ip_assignment.append(ip_assignment_item)



        ip_stack = []
        for ip_stack_item_data in self.ip_stack:
            ip_stack_item: str = ip_stack_item_data
            ip_stack.append(ip_stack_item)



        type_: str = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "802.1x": 802_1x,
            "internal": internal,
            "ipAssignment": ip_assignment,
            "ipStack": ip_stack,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        802_1x = d.pop("802.1x")

        internal = d.pop("internal")

        ip_assignment = []
        _ip_assignment = d.pop("ipAssignment")
        for ip_assignment_item_data in (_ip_assignment):
            ip_assignment_item = check_get_reader_capabilites_capabilities_network_interfaces_item_ip_assignment_item(ip_assignment_item_data)



            ip_assignment.append(ip_assignment_item)


        ip_stack = []
        _ip_stack = d.pop("ipStack")
        for ip_stack_item_data in (_ip_stack):
            ip_stack_item = check_get_reader_capabilites_capabilities_network_interfaces_item_ip_stack_item(ip_stack_item_data)



            ip_stack.append(ip_stack_item)


        type_ = check_get_reader_capabilites_capabilities_network_interfaces_item_type(d.pop("type"))




        get_reader_capabilites_capabilities_network_interfaces_item = cls(
            802_1x=802_1x,
            internal=internal,
            ip_assignment=ip_assignment,
            ip_stack=ip_stack,
            type_=type_,
        )


        get_reader_capabilites_capabilities_network_interfaces_item.additional_properties = d
        return get_reader_capabilites_capabilities_network_interfaces_item

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
