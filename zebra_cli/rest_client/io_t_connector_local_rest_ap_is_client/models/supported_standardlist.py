from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.supported_standardlist_supported_standards_item import SupportedStandardlistSupportedStandardsItem





T = TypeVar("T", bound="SupportedStandardlist")



@_attrs_define
class SupportedStandardlist:
    """ Represents the Supported Standard list configuration.

        Attributes:
            supported_standards (Union[Unset, list['SupportedStandardlistSupportedStandardsItem']]): Represents the
                Supported Standard list configuration.
     """

    supported_standards: Union[Unset, list['SupportedStandardlistSupportedStandardsItem']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.supported_standardlist_supported_standards_item import SupportedStandardlistSupportedStandardsItem
        supported_standards: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.supported_standards, Unset):
            supported_standards = []
            for supported_standards_item_data in self.supported_standards:
                supported_standards_item = supported_standards_item_data.to_dict()
                supported_standards.append(supported_standards_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if supported_standards is not UNSET:
            field_dict["SupportedStandards"] = supported_standards

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.supported_standardlist_supported_standards_item import SupportedStandardlistSupportedStandardsItem
        d = dict(src_dict)
        supported_standards = []
        _supported_standards = d.pop("SupportedStandards", UNSET)
        for supported_standards_item_data in (_supported_standards or []):
            supported_standards_item = SupportedStandardlistSupportedStandardsItem.from_dict(supported_standards_item_data)



            supported_standards.append(supported_standards_item)


        supported_standardlist = cls(
            supported_standards=supported_standards,
        )


        supported_standardlist.additional_properties = d
        return supported_standardlist

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
