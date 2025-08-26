from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.management_events_configuration_heartbeat_fields import ManagementEventsConfigurationHeartbeatFields





T = TypeVar("T", bound="ManagementEventsConfigurationHeartbeat")



@_attrs_define
class ManagementEventsConfigurationHeartbeat:
    """ Asynchronous Heartbeat Events

        Attributes:
            fields (ManagementEventsConfigurationHeartbeatFields): heartbeat fields
            interval (float): heartbeat report interval in seconds Default: 60.0.
     """

    fields: 'ManagementEventsConfigurationHeartbeatFields'
    interval: float = 60.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.management_events_configuration_heartbeat_fields import ManagementEventsConfigurationHeartbeatFields
        fields = self.fields.to_dict()

        interval = self.interval


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "fields": fields,
            "interval": interval,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.management_events_configuration_heartbeat_fields import ManagementEventsConfigurationHeartbeatFields
        d = dict(src_dict)
        fields = ManagementEventsConfigurationHeartbeatFields.from_dict(d.pop("fields"))




        interval = d.pop("interval")

        management_events_configuration_heartbeat = cls(
            fields=fields,
            interval=interval,
        )


        management_events_configuration_heartbeat.additional_properties = d
        return management_events_configuration_heartbeat

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
