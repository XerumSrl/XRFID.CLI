from typing import Literal, cast

RegionConfigMinTxPowerSupported = Literal[100]

REGION_CONFIG_MIN_TX_POWER_SUPPORTED_VALUES: set[RegionConfigMinTxPowerSupported] = { 100,  }

def check_region_config_min_tx_power_supported(value: int) -> RegionConfigMinTxPowerSupported:
    if value in REGION_CONFIG_MIN_TX_POWER_SUPPORTED_VALUES:
        return cast(RegionConfigMinTxPowerSupported, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {REGION_CONFIG_MIN_TX_POWER_SUPPORTED_VALUES!r}")
