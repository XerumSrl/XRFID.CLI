from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.endpoint_info_object_protocol import check_endpoint_info_object_protocol
from ..models.endpoint_info_object_protocol import EndpointInfoObjectProtocol
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="EndpointInfoObject")



@_attrs_define
class EndpointInfoObject:
    """ Configuration of MQTT Endpoint

        Attributes:
            host_name (str): Host name of the MQTT Connection Example: 10.17.231.77.
            port (int): Port Number of the MQTT Connection Example: 8883.
            protocol (Union[Unset, EndpointInfoObjectProtocol]): type of protocol to be used. If not provided tcp or ssl
                determined from enableSecurity flag.
     """

    host_name: str
    port: int
    protocol: Union[Unset, EndpointInfoObjectProtocol] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        host_name = self.host_name

        port = self.port

        protocol: Union[Unset, str] = UNSET
        if not isinstance(self.protocol, Unset):
            protocol = self.protocol



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "hostName": host_name,
            "port": port,
        })
        if protocol is not UNSET:
            field_dict["protocol"] = protocol

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        host_name = d.pop("hostName")

        port = d.pop("port")

        _protocol = d.pop("protocol", UNSET)
        protocol: Union[Unset, EndpointInfoObjectProtocol]
        if isinstance(_protocol,  Unset):
            protocol = UNSET
        else:
            protocol = check_endpoint_info_object_protocol(_protocol)




        endpoint_info_object = cls(
            host_name=host_name,
            port=port,
            protocol=protocol,
        )


        endpoint_info_object.additional_properties = d
        return endpoint_info_object

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
