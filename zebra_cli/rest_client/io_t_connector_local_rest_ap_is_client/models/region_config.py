from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.region_config_max_tx_power_supported import check_region_config_max_tx_power_supported
from ..models.region_config_max_tx_power_supported import RegionConfigMaxTxPowerSupported
from ..models.region_config_min_tx_power_supported import check_region_config_min_tx_power_supported
from ..models.region_config_min_tx_power_supported import RegionConfigMinTxPowerSupported
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="RegionConfig")



@_attrs_define
class RegionConfig:
    """ Represents the region and regulatory configuration.

        Attributes:
            region (str): The RF region of operation Example: US.
            lbt_enabled (bool): A flag indicating whether listen before talk is enabled Default: False. Example: false.
            regulatory_standard (Union[Unset, str]): The RF regulatory standard followed Example: FCC.
            channel_data (Union[Unset, list[float]]): The list of channels enabled Example: [915250, 915750, 903250, 926750,
                926250, 904250, 927250, 920250, 919250, 909250, 918750, 917750, 905250, 904750, 925250, 921750, 914750, 906750,
                913750, 922250, 911250, 911750, 903750, 908750, 905750, 912250, 906250, 917250, 914250, 907250, 918250, 916250,
                910250, 910750, 907750, 924750, 909750, 919750, 916750, 913250, 923750, 908250, 925750, 912750, 924250, 921250,
                920750, 922750, 902750, 923250].
            min_tx_power_supported (Union[Unset, RegionConfigMinTxPowerSupported]): Gets the minimum Transmit power of the
                reader Example: 100.
            max_tx_power_supported (Union[Unset, RegionConfigMaxTxPowerSupported]): Gets the maximum Transmit power of the
                reader Example: 300.
     """

    region: str
    lbt_enabled: bool = False
    regulatory_standard: Union[Unset, str] = UNSET
    channel_data: Union[Unset, list[float]] = UNSET
    min_tx_power_supported: Union[Unset, RegionConfigMinTxPowerSupported] = UNSET
    max_tx_power_supported: Union[Unset, RegionConfigMaxTxPowerSupported] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        region = self.region

        lbt_enabled = self.lbt_enabled

        regulatory_standard = self.regulatory_standard

        channel_data: Union[Unset, list[float]] = UNSET
        if not isinstance(self.channel_data, Unset):
            channel_data = self.channel_data



        min_tx_power_supported: Union[Unset, int] = UNSET
        if not isinstance(self.min_tx_power_supported, Unset):
            min_tx_power_supported = self.min_tx_power_supported


        max_tx_power_supported: Union[Unset, int] = UNSET
        if not isinstance(self.max_tx_power_supported, Unset):
            max_tx_power_supported = self.max_tx_power_supported



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "region": region,
            "lbtEnabled": lbt_enabled,
        })
        if regulatory_standard is not UNSET:
            field_dict["regulatoryStandard"] = regulatory_standard
        if channel_data is not UNSET:
            field_dict["channelData"] = channel_data
        if min_tx_power_supported is not UNSET:
            field_dict["minTxPowerSupported"] = min_tx_power_supported
        if max_tx_power_supported is not UNSET:
            field_dict["maxTxPowerSupported"] = max_tx_power_supported

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        region = d.pop("region")

        lbt_enabled = d.pop("lbtEnabled")

        regulatory_standard = d.pop("regulatoryStandard", UNSET)

        channel_data = cast(list[float], d.pop("channelData", UNSET))


        _min_tx_power_supported = d.pop("minTxPowerSupported", UNSET)
        min_tx_power_supported: Union[Unset, RegionConfigMinTxPowerSupported]
        if isinstance(_min_tx_power_supported,  Unset):
            min_tx_power_supported = UNSET
        else:
            min_tx_power_supported = check_region_config_min_tx_power_supported(_min_tx_power_supported)




        _max_tx_power_supported = d.pop("maxTxPowerSupported", UNSET)
        max_tx_power_supported: Union[Unset, RegionConfigMaxTxPowerSupported]
        if isinstance(_max_tx_power_supported,  Unset):
            max_tx_power_supported = UNSET
        else:
            max_tx_power_supported = check_region_config_max_tx_power_supported(_max_tx_power_supported)




        region_config = cls(
            region=region,
            lbt_enabled=lbt_enabled,
            regulatory_standard=regulatory_standard,
            channel_data=channel_data,
            min_tx_power_supported=min_tx_power_supported,
            max_tx_power_supported=max_tx_power_supported,
        )


        region_config.additional_properties = d
        return region_config

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
