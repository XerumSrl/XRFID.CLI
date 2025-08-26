from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="TagDataEventsBatchingConfiguration")



@_attrs_define
class TagDataEventsBatchingConfiguration:
    """ Tag Data Events batching configuration

        Attributes:
            reporting_interval (Union[Unset, float]): Event Report interval in milliseconds. -1 disables this option
                Example: 1000.
            max_payload_size_per_report (Union[Unset, float]): Maximum payload size in bytes. -1 disables Default: 256000.0.
     """

    reporting_interval: Union[Unset, float] = UNSET
    max_payload_size_per_report: Union[Unset, float] = 256000.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        reporting_interval = self.reporting_interval

        max_payload_size_per_report = self.max_payload_size_per_report


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if reporting_interval is not UNSET:
            field_dict["reportingInterval"] = reporting_interval
        if max_payload_size_per_report is not UNSET:
            field_dict["maxPayloadSizePerReport"] = max_payload_size_per_report

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reporting_interval = d.pop("reportingInterval", UNSET)

        max_payload_size_per_report = d.pop("maxPayloadSizePerReport", UNSET)

        tag_data_events_batching_configuration = cls(
            reporting_interval=reporting_interval,
            max_payload_size_per_report=max_payload_size_per_report,
        )


        tag_data_events_batching_configuration.additional_properties = d
        return tag_data_events_batching_configuration

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
