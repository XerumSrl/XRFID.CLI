from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.directionality_settings_basic_config_beams_beams_item import DirectionalitySettingsBasicConfigBeamsBeamsItem





T = TypeVar("T", bound="DirectionalitySettingsBasicConfigBeams")



@_attrs_define
class DirectionalitySettingsBasicConfigBeams:
    """ 
        Attributes:
            beams (Union[Unset, list['DirectionalitySettingsBasicConfigBeamsBeamsItem']]): Array of beams to use
     """

    beams: Union[Unset, list['DirectionalitySettingsBasicConfigBeamsBeamsItem']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.directionality_settings_basic_config_beams_beams_item import DirectionalitySettingsBasicConfigBeamsBeamsItem
        beams: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.beams, Unset):
            beams = []
            for beams_item_data in self.beams:
                beams_item = beams_item_data.to_dict()
                beams.append(beams_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if beams is not UNSET:
            field_dict["beams"] = beams

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.directionality_settings_basic_config_beams_beams_item import DirectionalitySettingsBasicConfigBeamsBeamsItem
        d = dict(src_dict)
        beams = []
        _beams = d.pop("beams", UNSET)
        for beams_item_data in (_beams or []):
            beams_item = DirectionalitySettingsBasicConfigBeamsBeamsItem.from_dict(beams_item_data)



            beams.append(beams_item)


        directionality_settings_basic_config_beams = cls(
            beams=beams,
        )


        directionality_settings_basic_config_beams.additional_properties = d
        return directionality_settings_basic_config_beams

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
