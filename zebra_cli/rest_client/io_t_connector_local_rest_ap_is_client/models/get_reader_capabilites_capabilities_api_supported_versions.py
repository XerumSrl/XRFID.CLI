from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_reader_capabilites_capabilities_api_supported_versions_version import check_get_reader_capabilites_capabilities_api_supported_versions_version
from ..models.get_reader_capabilites_capabilities_api_supported_versions_version import GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion
from typing import cast






T = TypeVar("T", bound="GetReaderCapabilitesCapabilitiesApiSupportedVersions")



@_attrs_define
class GetReaderCapabilitesCapabilitiesApiSupportedVersions:
    """ API Version information

        Attributes:
            documentation (str): Link to api documentation. Example: https://zebradevs.github.io/rfid-ziotc-
                docs/about/index.html.
            version (GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion): api version
     """

    documentation: str
    version: GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        documentation = self.documentation

        version: str = self.version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "documentation": documentation,
            "version": version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        documentation = d.pop("documentation")

        version = check_get_reader_capabilites_capabilities_api_supported_versions_version(d.pop("version"))




        get_reader_capabilites_capabilities_api_supported_versions = cls(
            documentation=documentation,
            version=version,
        )


        get_reader_capabilites_capabilities_api_supported_versions.additional_properties = d
        return get_reader_capabilites_capabilities_api_supported_versions

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
