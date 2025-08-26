from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="ManagementEventsConfigurationWarningsCpu")



@_attrs_define
class ManagementEventsConfigurationWarningsCpu:
    """ CPU Usage Warning Alerts

        Attributes:
            threshold (float): Warning CPU usage limit Default: 80.0. Example: 80.
            report_interval_in_sec (Union[Unset, float]): Warning Report Interval in seconds. Default: 1800.0. Example:
                1800.
     """

    threshold: float = 80.0
    report_interval_in_sec: Union[Unset, float] = 1800.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        threshold = self.threshold

        report_interval_in_sec = self.report_interval_in_sec


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "threshold": threshold,
        })
        if report_interval_in_sec is not UNSET:
            field_dict["reportIntervalInSec"] = report_interval_in_sec

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        threshold = d.pop("threshold")

        report_interval_in_sec = d.pop("reportIntervalInSec", UNSET)

        management_events_configuration_warnings_cpu = cls(
            threshold=threshold,
            report_interval_in_sec=report_interval_in_sec,
        )


        management_events_configuration_warnings_cpu.additional_properties = d
        return management_events_configuration_warnings_cpu

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
