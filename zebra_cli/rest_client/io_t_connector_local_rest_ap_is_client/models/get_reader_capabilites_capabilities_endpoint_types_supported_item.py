from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item_authentication_types_supported_item import check_get_reader_capabilites_capabilities_endpoint_types_supported_item_authentication_types_supported_item
from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item_authentication_types_supported_item import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem
from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item_type import check_get_reader_capabilites_capabilities_endpoint_types_supported_item_type
from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item_type import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType
from typing import cast






T = TypeVar("T", bound="GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem")



@_attrs_define
class GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem:
    """ 
        Attributes:
            ssl_supported (bool): Denotes if the reader supports SSL
            authentication_types_supported
                (list[GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem]): Types of
                authentication supported by the reader
            batching_supported (bool): Denotes if the reader supports Batching
            data_only (bool): Denotes if the endpoint is configured for data only
            retention_supported (bool): Denotes if the reader supports Retention
            type_ (GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType): type of endpoint
     """

    ssl_supported: bool
    authentication_types_supported: list[GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem]
    batching_supported: bool
    data_only: bool
    retention_supported: bool
    type_: GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ssl_supported = self.ssl_supported

        authentication_types_supported = []
        for authentication_types_supported_item_data in self.authentication_types_supported:
            authentication_types_supported_item: str = authentication_types_supported_item_data
            authentication_types_supported.append(authentication_types_supported_item)



        batching_supported = self.batching_supported

        data_only = self.data_only

        retention_supported = self.retention_supported

        type_: str = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "SSLSupported": ssl_supported,
            "authenticationTypesSupported": authentication_types_supported,
            "batchingSupported": batching_supported,
            "dataOnly": data_only,
            "retentionSupported": retention_supported,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ssl_supported = d.pop("SSLSupported")

        authentication_types_supported = []
        _authentication_types_supported = d.pop("authenticationTypesSupported")
        for authentication_types_supported_item_data in (_authentication_types_supported):
            authentication_types_supported_item = check_get_reader_capabilites_capabilities_endpoint_types_supported_item_authentication_types_supported_item(authentication_types_supported_item_data)



            authentication_types_supported.append(authentication_types_supported_item)


        batching_supported = d.pop("batchingSupported")

        data_only = d.pop("dataOnly")

        retention_supported = d.pop("retentionSupported")

        type_ = check_get_reader_capabilites_capabilities_endpoint_types_supported_item_type(d.pop("type"))




        get_reader_capabilites_capabilities_endpoint_types_supported_item = cls(
            ssl_supported=ssl_supported,
            authentication_types_supported=authentication_types_supported,
            batching_supported=batching_supported,
            data_only=data_only,
            retention_supported=retention_supported,
            type_=type_,
        )


        get_reader_capabilites_capabilities_endpoint_types_supported_item.additional_properties = d
        return get_reader_capabilites_capabilities_endpoint_types_supported_item

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
