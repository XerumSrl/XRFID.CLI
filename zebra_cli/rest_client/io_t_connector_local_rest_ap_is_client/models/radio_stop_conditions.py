from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.gpi import Gpi





T = TypeVar("T", bound="RadioStopConditions")



@_attrs_define
class RadioStopConditions:
    """ Controls when an ongoing operation completes.

    If absent, the radio will continue trying to inventory tags until a "stop" is issued.

        Attributes:
            duration (Union[Unset, int]): Time to run until radio stops (in seconds)
            antenna_cycles (Union[Unset, int]): The number of cycles through all enabled antennas before stopping the radio
            tag_count (Union[Unset, int]): The number of tags to inventory until the radio stops. Cannot be set at the same
                time as durationAfterNoMoreUniqueTags
            duration_after_no_more_unique_tags (Union[Unset, int]): Duration (in seconds) after not inventorying any more
                unique tags to stop the radio. Cannot be set at the same time as tagCount
            gpis (Union[Unset, list['Gpi']]):
     """

    duration: Union[Unset, int] = UNSET
    antenna_cycles: Union[Unset, int] = UNSET
    tag_count: Union[Unset, int] = UNSET
    duration_after_no_more_unique_tags: Union[Unset, int] = UNSET
    gpis: Union[Unset, list['Gpi']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.gpi import Gpi
        duration = self.duration

        antenna_cycles = self.antenna_cycles

        tag_count = self.tag_count

        duration_after_no_more_unique_tags = self.duration_after_no_more_unique_tags

        gpis: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.gpis, Unset):
            gpis = []
            for gpis_item_data in self.gpis:
                gpis_item = gpis_item_data.to_dict()
                gpis.append(gpis_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if duration is not UNSET:
            field_dict["duration"] = duration
        if antenna_cycles is not UNSET:
            field_dict["antennaCycles"] = antenna_cycles
        if tag_count is not UNSET:
            field_dict["tagCount"] = tag_count
        if duration_after_no_more_unique_tags is not UNSET:
            field_dict["durationAfterNoMoreUniqueTags"] = duration_after_no_more_unique_tags
        if gpis is not UNSET:
            field_dict["gpis"] = gpis

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gpi import Gpi
        d = dict(src_dict)
        duration = d.pop("duration", UNSET)

        antenna_cycles = d.pop("antennaCycles", UNSET)

        tag_count = d.pop("tagCount", UNSET)

        duration_after_no_more_unique_tags = d.pop("durationAfterNoMoreUniqueTags", UNSET)

        gpis = []
        _gpis = d.pop("gpis", UNSET)
        for gpis_item_data in (_gpis or []):
            gpis_item = Gpi.from_dict(gpis_item_data)



            gpis.append(gpis_item)


        radio_stop_conditions = cls(
            duration=duration,
            antenna_cycles=antenna_cycles,
            tag_count=tag_count,
            duration_after_no_more_unique_tags=duration_after_no_more_unique_tags,
            gpis=gpis,
        )


        radio_stop_conditions.additional_properties = d
        return radio_stop_conditions

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
