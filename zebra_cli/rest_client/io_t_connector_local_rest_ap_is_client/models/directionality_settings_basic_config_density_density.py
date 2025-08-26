from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.directionality_settings_basic_config_density_density_polarization import check_directionality_settings_basic_config_density_density_polarization
from ..models.directionality_settings_basic_config_density_density_polarization import DirectionalitySettingsBasicConfigDensityDensityPolarization
from ..models.directionality_settings_basic_config_density_density_type import check_directionality_settings_basic_config_density_density_type
from ..models.directionality_settings_basic_config_density_density_type import DirectionalitySettingsBasicConfigDensityDensityType
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="DirectionalitySettingsBasicConfigDensityDensity")



@_attrs_define
class DirectionalitySettingsBasicConfigDensityDensity:
    """ 
        Attributes:
            type_ (DirectionalitySettingsBasicConfigDensityDensityType): Type of density of Beams Default: 'DEFAULT'.
            polarization (Union[Unset, DirectionalitySettingsBasicConfigDensityDensityPolarization]): Polarization of beams
                Default: 'LHCP'.
     """

    type_: DirectionalitySettingsBasicConfigDensityDensityType = 'DEFAULT'
    polarization: Union[Unset, DirectionalitySettingsBasicConfigDensityDensityPolarization] = 'LHCP'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        polarization: Union[Unset, str] = UNSET
        if not isinstance(self.polarization, Unset):
            polarization = self.polarization



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if polarization is not UNSET:
            field_dict["polarization"] = polarization

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_directionality_settings_basic_config_density_density_type(d.pop("type"))




        _polarization = d.pop("polarization", UNSET)
        polarization: Union[Unset, DirectionalitySettingsBasicConfigDensityDensityPolarization]
        if isinstance(_polarization,  Unset):
            polarization = UNSET
        else:
            polarization = check_directionality_settings_basic_config_density_density_polarization(_polarization)




        directionality_settings_basic_config_density_density = cls(
            type_=type_,
            polarization=polarization,
        )


        directionality_settings_basic_config_density_density.additional_properties = d
        return directionality_settings_basic_config_density_density

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
