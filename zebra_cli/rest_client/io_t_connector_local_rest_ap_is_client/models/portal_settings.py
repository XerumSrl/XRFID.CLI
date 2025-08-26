from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.portal_settings_start_trigger import PortalSettingsStartTrigger





T = TypeVar("T", bound="PortalSettings")



@_attrs_define
class PortalSettings:
    """ Reader settings for portal mode.

    Note : port 3 and 4 supported in FX9600 device only

        Attributes:
            start_trigger (Union[Unset, PortalSettingsStartTrigger]): The GPI trigger to start reads on the portal
            stop_interval (Union[Unset, int]): The interval at which to stop reads after the last unique tag is read
                (seconds). If absent, the reader will stop after not reading a unique tag in 3 seconds
     """

    start_trigger: Union[Unset, 'PortalSettingsStartTrigger'] = UNSET
    stop_interval: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.portal_settings_start_trigger import PortalSettingsStartTrigger
        start_trigger: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start_trigger, Unset):
            start_trigger = self.start_trigger.to_dict()

        stop_interval = self.stop_interval


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if start_trigger is not UNSET:
            field_dict["startTrigger"] = start_trigger
        if stop_interval is not UNSET:
            field_dict["stopInterval"] = stop_interval

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.portal_settings_start_trigger import PortalSettingsStartTrigger
        d = dict(src_dict)
        _start_trigger = d.pop("startTrigger", UNSET)
        start_trigger: Union[Unset, PortalSettingsStartTrigger]
        if isinstance(_start_trigger,  Unset):
            start_trigger = UNSET
        else:
            start_trigger = PortalSettingsStartTrigger.from_dict(_start_trigger)




        stop_interval = d.pop("stopInterval", UNSET)

        portal_settings = cls(
            start_trigger=start_trigger,
            stop_interval=stop_interval,
        )


        portal_settings.additional_properties = d
        return portal_settings

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
