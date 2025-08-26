from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="TagDataEventsRetentionConfiguration")



@_attrs_define
class TagDataEventsRetentionConfiguration:
    """ Tag Data Events Retention Configuration on connection lost

        Attributes:
            throttle (Union[Unset, int]): Rate (in events per second) to report data events when network is reconnected
                Default: 500. Example: 200.
            max_num_events (Union[Unset, int]): Maximum number of events to retain Default: 150000. Example: 150000.
            max_event_retention_time_in_min (Union[Unset, float]): Maximum event retention time (in minutes)

                0 or -1 indicate Events will be retained Forever.
                -1 is the default

                Example:
                10 indicate Events generated in last 10 minutes will be retained Default: 0.0. Example: 10.
     """

    throttle: Union[Unset, int] = 500
    max_num_events: Union[Unset, int] = 150000
    max_event_retention_time_in_min: Union[Unset, float] = 0.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        throttle = self.throttle

        max_num_events = self.max_num_events

        max_event_retention_time_in_min = self.max_event_retention_time_in_min


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if throttle is not UNSET:
            field_dict["throttle"] = throttle
        if max_num_events is not UNSET:
            field_dict["maxNumEvents"] = max_num_events
        if max_event_retention_time_in_min is not UNSET:
            field_dict["maxEventRetentionTimeInMin"] = max_event_retention_time_in_min

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        throttle = d.pop("throttle", UNSET)

        max_num_events = d.pop("maxNumEvents", UNSET)

        max_event_retention_time_in_min = d.pop("maxEventRetentionTimeInMin", UNSET)

        tag_data_events_retention_configuration = cls(
            throttle=throttle,
            max_num_events=max_num_events,
            max_event_retention_time_in_min=max_event_retention_time_in_min,
        )


        tag_data_events_retention_configuration.additional_properties = d
        return tag_data_events_retention_configuration

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
