from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.directionality_settings_aar import DirectionalitySettingsAar
  from ..models.directionality_settings_basic_config import DirectionalitySettingsBasicConfig
  from ..models.directionality_settings_advanced_config import DirectionalitySettingsAdvancedConfig





T = TypeVar("T", bound="DirectionalitySettings")



@_attrs_define
class DirectionalitySettings:
    """ directionality mode settings

        Attributes:
            basic_config (DirectionalitySettingsBasicConfig): Basic Configuration
                This Basic Configuration is a superset of standard ZIOTC operating mode
            advanced_config (DirectionalitySettingsAdvancedConfig): Advanced Directionality Configuration
            aar (Union[Unset, DirectionalitySettingsAar]): ATR information for 2 ATR Directionality
     """

    basic_config: 'DirectionalitySettingsBasicConfig'
    advanced_config: 'DirectionalitySettingsAdvancedConfig'
    aar: Union[Unset, 'DirectionalitySettingsAar'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.directionality_settings_aar import DirectionalitySettingsAar
        from ..models.directionality_settings_basic_config import DirectionalitySettingsBasicConfig
        from ..models.directionality_settings_advanced_config import DirectionalitySettingsAdvancedConfig
        basic_config = self.basic_config.to_dict()

        advanced_config = self.advanced_config.to_dict()

        aar: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aar, Unset):
            aar = self.aar.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "basicConfig": basic_config,
            "advancedConfig": advanced_config,
        })
        if aar is not UNSET:
            field_dict["aar"] = aar

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.directionality_settings_aar import DirectionalitySettingsAar
        from ..models.directionality_settings_basic_config import DirectionalitySettingsBasicConfig
        from ..models.directionality_settings_advanced_config import DirectionalitySettingsAdvancedConfig
        d = dict(src_dict)
        basic_config = DirectionalitySettingsBasicConfig.from_dict(d.pop("basicConfig"))




        advanced_config = DirectionalitySettingsAdvancedConfig.from_dict(d.pop("advancedConfig"))




        _aar = d.pop("aar", UNSET)
        aar: Union[Unset, DirectionalitySettingsAar]
        if isinstance(_aar,  Unset):
            aar = UNSET
        else:
            aar = DirectionalitySettingsAar.from_dict(_aar)




        directionality_settings = cls(
            basic_config=basic_config,
            advanced_config=advanced_config,
            aar=aar,
        )


        directionality_settings.additional_properties = d
        return directionality_settings

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
