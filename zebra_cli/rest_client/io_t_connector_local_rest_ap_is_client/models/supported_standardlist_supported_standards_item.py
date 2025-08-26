from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="SupportedStandardlistSupportedStandardsItem")



@_attrs_define
class SupportedStandardlistSupportedStandardsItem:
    """ 
        Attributes:
            standard_name (Union[Unset, str]): The RF regulatory standard followed Default: 'UNDEFINED'. Example: Argentina.
            is_lbt_configurable (Union[Unset, bool]): A flag indicating whether listen before talk is enabled Default:
                False. Example: false.
            channel_data (Union[Unset, list[float]]): The list of channels enabled Example: [915250, 915750, 903250, 926750,
                926250, 904250, 927250, 920250, 919250, 909250, 918750, 917750, 905250, 904750, 925250, 921750, 914750, 906750,
                913750, 922250, 911250, 911750, 903750, 908750, 905750, 912250, 906250, 917250, 914250, 907250, 918250, 916250,
                910250, 910750, 907750, 924750, 909750, 919750, 916750, 913250, 923750, 908250, 925750, 912750, 924250, 921250,
                920750, 922750, 902750, 923250].
            is_hopping_configurable (Union[Unset, bool]): A flag indicating whether channel selection is enabled Default:
                False. Example: false.
     """

    standard_name: Union[Unset, str] = 'UNDEFINED'
    is_lbt_configurable: Union[Unset, bool] = False
    channel_data: Union[Unset, list[float]] = UNSET
    is_hopping_configurable: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        standard_name = self.standard_name

        is_lbt_configurable = self.is_lbt_configurable

        channel_data: Union[Unset, list[float]] = UNSET
        if not isinstance(self.channel_data, Unset):
            channel_data = self.channel_data



        is_hopping_configurable = self.is_hopping_configurable


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if standard_name is not UNSET:
            field_dict["StandardName"] = standard_name
        if is_lbt_configurable is not UNSET:
            field_dict["isLBTConfigurable"] = is_lbt_configurable
        if channel_data is not UNSET:
            field_dict["channelData"] = channel_data
        if is_hopping_configurable is not UNSET:
            field_dict["isHoppingConfigurable"] = is_hopping_configurable

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        standard_name = d.pop("StandardName", UNSET)

        is_lbt_configurable = d.pop("isLBTConfigurable", UNSET)

        channel_data = cast(list[float], d.pop("channelData", UNSET))


        is_hopping_configurable = d.pop("isHoppingConfigurable", UNSET)

        supported_standardlist_supported_standards_item = cls(
            standard_name=standard_name,
            is_lbt_configurable=is_lbt_configurable,
            channel_data=channel_data,
            is_hopping_configurable=is_hopping_configurable,
        )


        supported_standardlist_supported_standards_item.additional_properties = d
        return supported_standardlist_supported_standards_item

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
