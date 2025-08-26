from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.directionality_settings_basic_config_density_density import DirectionalitySettingsBasicConfigDensityDensity





T = TypeVar("T", bound="DirectionalitySettingsBasicConfigDensity")



@_attrs_define
class DirectionalitySettingsBasicConfigDensity:
    """ 
        Attributes:
            density (Union[Unset, DirectionalitySettingsBasicConfigDensityDensity]):
     """

    density: Union[Unset, 'DirectionalitySettingsBasicConfigDensityDensity'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.directionality_settings_basic_config_density_density import DirectionalitySettingsBasicConfigDensityDensity
        density: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.density, Unset):
            density = self.density.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if density is not UNSET:
            field_dict["density"] = density

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.directionality_settings_basic_config_density_density import DirectionalitySettingsBasicConfigDensityDensity
        d = dict(src_dict)
        _density = d.pop("density", UNSET)
        density: Union[Unset, DirectionalitySettingsBasicConfigDensityDensity]
        if isinstance(_density,  Unset):
            density = UNSET
        else:
            density = DirectionalitySettingsBasicConfigDensityDensity.from_dict(_density)




        directionality_settings_basic_config_density = cls(
            density=density,
        )


        directionality_settings_basic_config_density.additional_properties = d
        return directionality_settings_basic_config_density

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
