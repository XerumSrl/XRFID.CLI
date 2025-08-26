from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="GetSupportedRegionList")



@_attrs_define
class GetSupportedRegionList:
    """ Retrieves the region list supported by the reader based on the readertype

        Attributes:
            supported_regions (Union[Unset, list[str]]): It contains SupportedRegions array with list of countries supported
                by the reader Example: ['Argentina', 'Australia', 'Bangladesh', 'Brazil', 'Cambodia', 'Canada', 'China',
                'Colombia', 'Costa', 'Rica', 'European', 'Union', 'Ghana', 'Hong Kong', 'India', 'Indonesia', 'Jordan', 'Korea',
                'Laos', 'Malaysia', 'Mexico', 'Morocco', 'New Zealand', 'Peru', 'Philippines', 'Russia', 'Saudi Arabia',
                'Singapore', 'South Africa', 'Taiwan', 'UAE', 'Ukraine', 'Venezuela', 'Vietnam'].
     """

    supported_regions: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        supported_regions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.supported_regions, Unset):
            supported_regions = self.supported_regions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if supported_regions is not UNSET:
            field_dict["SupportedRegions"] = supported_regions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        supported_regions = cast(list[str], d.pop("SupportedRegions", UNSET))


        get_supported_region_list = cls(
            supported_regions=supported_regions,
        )


        get_supported_region_list.additional_properties = d
        return get_supported_region_list

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
