from typing import Literal, cast

RegionConfigMaxTxPowerSupported = Literal[300]

REGION_CONFIG_MAX_TX_POWER_SUPPORTED_VALUES: set[RegionConfigMaxTxPowerSupported] = { 300,  }

def check_region_config_max_tx_power_supported(value: int) -> RegionConfigMaxTxPowerSupported:
    if value in REGION_CONFIG_MAX_TX_POWER_SUPPORTED_VALUES:
        return cast(RegionConfigMaxTxPowerSupported, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {REGION_CONFIG_MAX_TX_POWER_SUPPORTED_VALUES!r}")
