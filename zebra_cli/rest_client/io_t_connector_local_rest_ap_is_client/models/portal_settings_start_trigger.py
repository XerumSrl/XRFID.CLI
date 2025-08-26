from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.portal_settings_start_trigger_port import check_portal_settings_start_trigger_port
from ..models.portal_settings_start_trigger_port import PortalSettingsStartTriggerPort
from ..models.portal_settings_start_trigger_signal import check_portal_settings_start_trigger_signal
from ..models.portal_settings_start_trigger_signal import PortalSettingsStartTriggerSignal
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="PortalSettingsStartTrigger")



@_attrs_define
class PortalSettingsStartTrigger:
    """ The GPI trigger to start reads on the portal

        Attributes:
            port (Union[Unset, PortalSettingsStartTriggerPort]): The GPI port to signal. If absent, port 1 is used. Example:
                1.
            signal (Union[Unset, PortalSettingsStartTriggerSignal]): The signal value for the trigger. If absent, signal LOW
                is used
     """

    port: Union[Unset, PortalSettingsStartTriggerPort] = UNSET
    signal: Union[Unset, PortalSettingsStartTriggerSignal] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        port: Union[Unset, int] = UNSET
        if not isinstance(self.port, Unset):
            port = self.port


        signal: Union[Unset, str] = UNSET
        if not isinstance(self.signal, Unset):
            signal = self.signal



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if port is not UNSET:
            field_dict["port"] = port
        if signal is not UNSET:
            field_dict["signal"] = signal

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _port = d.pop("port", UNSET)
        port: Union[Unset, PortalSettingsStartTriggerPort]
        if isinstance(_port,  Unset):
            port = UNSET
        else:
            port = check_portal_settings_start_trigger_port(_port)




        _signal = d.pop("signal", UNSET)
        signal: Union[Unset, PortalSettingsStartTriggerSignal]
        if isinstance(_signal,  Unset):
            signal = UNSET
        else:
            signal = check_portal_settings_start_trigger_signal(_signal)




        portal_settings_start_trigger = cls(
            port=port,
            signal=signal,
        )


        portal_settings_start_trigger.additional_properties = d
        return portal_settings_start_trigger

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
