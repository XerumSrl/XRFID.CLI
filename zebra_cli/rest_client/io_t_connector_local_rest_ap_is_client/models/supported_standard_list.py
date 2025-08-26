from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.supported_standard_list_region import check_supported_standard_list_region
from ..models.supported_standard_list_region import SupportedStandardListRegion
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="SupportedStandardList")



@_attrs_define
class SupportedStandardList:
    """ Based on the region name provoided it gives the channel list

        Attributes:
            region (Union[Unset, SupportedStandardListRegion]): provide the region name  Example: Argentina.
     """

    region: Union[Unset, SupportedStandardListRegion] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        region: Union[Unset, str] = UNSET
        if not isinstance(self.region, Unset):
            region = self.region



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _region = d.pop("region", UNSET)
        region: Union[Unset, SupportedStandardListRegion]
        if isinstance(_region,  Unset):
            region = UNSET
        else:
            region = check_supported_standard_list_region(_region)




        supported_standard_list = cls(
            region=region,
        )


        supported_standard_list.additional_properties = d
        return supported_standard_list

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
