from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reader_interface_connection_status_data_item_connection_status import check_reader_interface_connection_status_data_item_connection_status
from ..models.reader_interface_connection_status_data_item_connection_status import ReaderInterfaceConnectionStatusDataItemConnectionStatus
from typing import cast






T = TypeVar("T", bound="ReaderInterfaceConnectionStatusDataItem")



@_attrs_define
class ReaderInterfaceConnectionStatusDataItem:
    """ 
        Attributes:
            connection_error (str): connection Error message Example: Sending DATA#2 to HTTP post server Failed:Couldnt
                connect to server(7).
            connection_status (ReaderInterfaceConnectionStatusDataItemConnectionStatus): Connection status of the data
                interface Example: disconnected.
            description (str): Data Endpoint description. Example: mqtt ws.
            interface (str): Unique Data Endpoint configuration name. Example: mqtt ws.
     """

    connection_error: str
    connection_status: ReaderInterfaceConnectionStatusDataItemConnectionStatus
    description: str
    interface: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_error = self.connection_error

        connection_status: str = self.connection_status

        description = self.description

        interface = self.interface


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connectionError": connection_error,
            "connectionStatus": connection_status,
            "description": description,
            "interface": interface,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_error = d.pop("connectionError")

        connection_status = check_reader_interface_connection_status_data_item_connection_status(d.pop("connectionStatus"))




        description = d.pop("description")

        interface = d.pop("interface")

        reader_interface_connection_status_data_item = cls(
            connection_error=connection_error,
            connection_status=connection_status,
            description=description,
            interface=interface,
        )


        reader_interface_connection_status_data_item.additional_properties = d
        return reader_interface_connection_status_data_item

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
