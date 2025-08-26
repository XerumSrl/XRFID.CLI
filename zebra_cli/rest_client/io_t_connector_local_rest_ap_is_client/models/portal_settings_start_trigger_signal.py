from typing import Literal, cast

PortalSettingsStartTriggerSignal = Literal['HIGH', 'LOW']

PORTAL_SETTINGS_START_TRIGGER_SIGNAL_VALUES: set[PortalSettingsStartTriggerSignal] = { 'HIGH', 'LOW',  }

def check_portal_settings_start_trigger_signal(value: str) -> PortalSettingsStartTriggerSignal:
    if value in PORTAL_SETTINGS_START_TRIGGER_SIGNAL_VALUES:
        return cast(PortalSettingsStartTriggerSignal, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PORTAL_SETTINGS_START_TRIGGER_SIGNAL_VALUES!r}")
