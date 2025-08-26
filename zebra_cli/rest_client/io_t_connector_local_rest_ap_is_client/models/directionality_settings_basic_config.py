from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.directionality_settings_basic_config_zone_plan import check_directionality_settings_basic_config_zone_plan
from ..models.directionality_settings_basic_config_zone_plan import DirectionalitySettingsBasicConfigZonePlan
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.directionality_settings_basic_config_beams import DirectionalitySettingsBasicConfigBeams
  from ..models.directionality_settings_basic_config_density import DirectionalitySettingsBasicConfigDensity





T = TypeVar("T", bound="DirectionalitySettingsBasicConfig")



@_attrs_define
class DirectionalitySettingsBasicConfig:
    """ Basic Configuration
    This Basic Configuration is a superset of standard ZIOTC operating mode

        Attributes:
            reader_height (Union[Unset, float]): Height of reader (in feet) Default: 15.0.
            tag_height (Union[Unset, float]): Height of tag (in feet) Default: 3.0.
            orientation (Union[Unset, float]): Orientation of the Zone Map North with respect to the ATR North (in degrees,
                clockwise) Default: 0.0.
            zone_plan (Union[Unset, DirectionalitySettingsBasicConfigZonePlan]): 4 or 6 zone zone plan Default: 4.
            inner_zone_width (Union[Unset, float]): The width of the main zones (in feet) Default: 10.0.
            zone_extension (Union[Unset, float]): The extension of the main zone into one another (in feet) Default: 0.0.
            beam_config (Union['DirectionalitySettingsBasicConfigBeams', 'DirectionalitySettingsBasicConfigDensity',
                Unset]):
            zone_names (Union[Unset, list[str]]): User defined names to zones. Array must have the same number of zones as
                specified in the zone plan
     """

    reader_height: Union[Unset, float] = 15.0
    tag_height: Union[Unset, float] = 3.0
    orientation: Union[Unset, float] = 0.0
    zone_plan: Union[Unset, DirectionalitySettingsBasicConfigZonePlan] = 4
    inner_zone_width: Union[Unset, float] = 10.0
    zone_extension: Union[Unset, float] = 0.0
    beam_config: Union['DirectionalitySettingsBasicConfigBeams', 'DirectionalitySettingsBasicConfigDensity', Unset] = UNSET
    zone_names: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.directionality_settings_basic_config_beams import DirectionalitySettingsBasicConfigBeams
        from ..models.directionality_settings_basic_config_density import DirectionalitySettingsBasicConfigDensity
        reader_height = self.reader_height

        tag_height = self.tag_height

        orientation = self.orientation

        zone_plan: Union[Unset, int] = UNSET
        if not isinstance(self.zone_plan, Unset):
            zone_plan = self.zone_plan


        inner_zone_width = self.inner_zone_width

        zone_extension = self.zone_extension

        beam_config: Union[Unset, dict[str, Any]]
        if isinstance(self.beam_config, Unset):
            beam_config = UNSET
        elif isinstance(self.beam_config, DirectionalitySettingsBasicConfigDensity):
            beam_config = self.beam_config.to_dict()
        else:
            beam_config = self.beam_config.to_dict()


        zone_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.zone_names, Unset):
            zone_names = self.zone_names




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if reader_height is not UNSET:
            field_dict["readerHeight"] = reader_height
        if tag_height is not UNSET:
            field_dict["tagHeight"] = tag_height
        if orientation is not UNSET:
            field_dict["orientation"] = orientation
        if zone_plan is not UNSET:
            field_dict["zonePlan"] = zone_plan
        if inner_zone_width is not UNSET:
            field_dict["innerZoneWidth"] = inner_zone_width
        if zone_extension is not UNSET:
            field_dict["zoneExtension"] = zone_extension
        if beam_config is not UNSET:
            field_dict["beamConfig"] = beam_config
        if zone_names is not UNSET:
            field_dict["zoneNames"] = zone_names

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.directionality_settings_basic_config_beams import DirectionalitySettingsBasicConfigBeams
        from ..models.directionality_settings_basic_config_density import DirectionalitySettingsBasicConfigDensity
        d = dict(src_dict)
        reader_height = d.pop("readerHeight", UNSET)

        tag_height = d.pop("tagHeight", UNSET)

        orientation = d.pop("orientation", UNSET)

        _zone_plan = d.pop("zonePlan", UNSET)
        zone_plan: Union[Unset, DirectionalitySettingsBasicConfigZonePlan]
        if isinstance(_zone_plan,  Unset):
            zone_plan = UNSET
        else:
            zone_plan = check_directionality_settings_basic_config_zone_plan(_zone_plan)




        inner_zone_width = d.pop("innerZoneWidth", UNSET)

        zone_extension = d.pop("zoneExtension", UNSET)

        def _parse_beam_config(data: object) -> Union['DirectionalitySettingsBasicConfigBeams', 'DirectionalitySettingsBasicConfigDensity', Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                beam_config_type_0_type_0 = DirectionalitySettingsBasicConfigDensity.from_dict(data)



                return beam_config_type_0_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            beam_config_type_1 = DirectionalitySettingsBasicConfigBeams.from_dict(data)



            return beam_config_type_1

        beam_config = _parse_beam_config(d.pop("beamConfig", UNSET))


        zone_names = cast(list[str], d.pop("zoneNames", UNSET))


        directionality_settings_basic_config = cls(
            reader_height=reader_height,
            tag_height=tag_height,
            orientation=orientation,
            zone_plan=zone_plan,
            inner_zone_width=inner_zone_width,
            zone_extension=zone_extension,
            beam_config=beam_config,
            zone_names=zone_names,
        )


        directionality_settings_basic_config.additional_properties = d
        return directionality_settings_basic_config

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
