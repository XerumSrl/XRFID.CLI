from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.management_events_configuration_errors import ManagementEventsConfigurationErrors
  from ..models.management_events_configuration_warnings import ManagementEventsConfigurationWarnings
  from ..models.management_events_configuration_heartbeat import ManagementEventsConfigurationHeartbeat





T = TypeVar("T", bound="ManagementEventsConfiguration")



@_attrs_define
class ManagementEventsConfiguration:
    """ Asynchronous management events configuration

        Attributes:
            errors (Union[Unset, ManagementEventsConfigurationErrors]): Asynchronous Management Errors
            warnings (Union[Unset, ManagementEventsConfigurationWarnings]): Asynchronous Management Warnings
            heartbeat (Union[Unset, ManagementEventsConfigurationHeartbeat]): Asynchronous Heartbeat Events
            gpi_events (Union[Unset, bool]): GPI Events Default: True.
            userapp_events (Union[Unset, bool]): asyncronous events from user applications  Default: True.
            gpo_events (Union[Unset, bool]): GPO Events Default: True.
     """

    errors: Union[Unset, 'ManagementEventsConfigurationErrors'] = UNSET
    warnings: Union[Unset, 'ManagementEventsConfigurationWarnings'] = UNSET
    heartbeat: Union[Unset, 'ManagementEventsConfigurationHeartbeat'] = UNSET
    gpi_events: Union[Unset, bool] = True
    userapp_events: Union[Unset, bool] = True
    gpo_events: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.management_events_configuration_errors import ManagementEventsConfigurationErrors
        from ..models.management_events_configuration_warnings import ManagementEventsConfigurationWarnings
        from ..models.management_events_configuration_heartbeat import ManagementEventsConfigurationHeartbeat
        errors: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        warnings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings.to_dict()

        heartbeat: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.heartbeat, Unset):
            heartbeat = self.heartbeat.to_dict()

        gpi_events = self.gpi_events

        userapp_events = self.userapp_events

        gpo_events = self.gpo_events


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if errors is not UNSET:
            field_dict["errors"] = errors
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if heartbeat is not UNSET:
            field_dict["heartbeat"] = heartbeat
        if gpi_events is not UNSET:
            field_dict["gpiEvents"] = gpi_events
        if userapp_events is not UNSET:
            field_dict["userappEvents"] = userapp_events
        if gpo_events is not UNSET:
            field_dict["gpoEvents"] = gpo_events

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.management_events_configuration_errors import ManagementEventsConfigurationErrors
        from ..models.management_events_configuration_warnings import ManagementEventsConfigurationWarnings
        from ..models.management_events_configuration_heartbeat import ManagementEventsConfigurationHeartbeat
        d = dict(src_dict)
        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, ManagementEventsConfigurationErrors]
        if isinstance(_errors,  Unset):
            errors = UNSET
        else:
            errors = ManagementEventsConfigurationErrors.from_dict(_errors)




        _warnings = d.pop("warnings", UNSET)
        warnings: Union[Unset, ManagementEventsConfigurationWarnings]
        if isinstance(_warnings,  Unset):
            warnings = UNSET
        else:
            warnings = ManagementEventsConfigurationWarnings.from_dict(_warnings)




        _heartbeat = d.pop("heartbeat", UNSET)
        heartbeat: Union[Unset, ManagementEventsConfigurationHeartbeat]
        if isinstance(_heartbeat,  Unset):
            heartbeat = UNSET
        else:
            heartbeat = ManagementEventsConfigurationHeartbeat.from_dict(_heartbeat)




        gpi_events = d.pop("gpiEvents", UNSET)

        userapp_events = d.pop("userappEvents", UNSET)

        gpo_events = d.pop("gpoEvents", UNSET)

        management_events_configuration = cls(
            errors=errors,
            warnings=warnings,
            heartbeat=heartbeat,
            gpi_events=gpi_events,
            userapp_events=userapp_events,
            gpo_events=gpo_events,
        )


        management_events_configuration.additional_properties = d
        return management_events_configuration

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
