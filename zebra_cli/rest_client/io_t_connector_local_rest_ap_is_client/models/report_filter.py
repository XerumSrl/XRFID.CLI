from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.report_filter_type import check_report_filter_type
from ..models.report_filter_type import ReportFilterType
from typing import cast






T = TypeVar("T", bound="ReportFilter")



@_attrs_define
class ReportFilter:
    """ Controls when and how often a tag is reported

    NOTE: This cannot be set while in "INVENTORY" mode. Setting the modeSpecificSetting for interval must be used in
    "INVENTORY" mode.

    If absent, each mode uses a different default.

    "SIMPLE": report tag read once.

    "PORTAL" and "CONVEYOR": report each tag the first time it is read on each antenna.

        Attributes:
            duration (int): Duration (in seconds) to wait to report a tag again once it has already been reported
                It should be noted that the way the filter works is that as long as the tag is being read by the reader, it will
                not report unless the time since the previous report of this tag on this antenna meets the type and duration.
                Duration is a uint32 value and the max value is bound by the data type.
            type_ (ReportFilterType): Configures the timeout (in seconds) by antenna or for entire radio
     """

    duration: int
    type_: ReportFilterType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        type_: str = self.type_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "duration": duration,
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration = d.pop("duration")

        type_ = check_report_filter_type(d.pop("type"))




        report_filter = cls(
            duration=duration,
            type_=type_,
        )


        report_filter.additional_properties = d
        return report_filter

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
