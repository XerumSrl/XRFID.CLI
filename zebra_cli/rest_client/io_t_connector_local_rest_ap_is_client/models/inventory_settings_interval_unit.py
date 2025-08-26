from typing import Literal, cast

InventorySettingsIntervalUnit = Literal['days', 'hours', 'minutes', 'seconds']

INVENTORY_SETTINGS_INTERVAL_UNIT_VALUES: set[InventorySettingsIntervalUnit] = { 'days', 'hours', 'minutes', 'seconds',  }

def check_inventory_settings_interval_unit(value: str) -> InventorySettingsIntervalUnit:
    if value in INVENTORY_SETTINGS_INTERVAL_UNIT_VALUES:
        return cast(InventorySettingsIntervalUnit, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INVENTORY_SETTINGS_INTERVAL_UNIT_VALUES!r}")
