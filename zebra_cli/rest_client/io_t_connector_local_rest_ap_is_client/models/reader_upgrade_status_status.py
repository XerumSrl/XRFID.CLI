from typing import Literal, cast

ReaderUpgradeStatusStatus = Literal['rebooting']

READER_UPGRADE_STATUS_STATUS_VALUES: set[ReaderUpgradeStatusStatus] = { 'rebooting',  }

def check_reader_upgrade_status_status(value: str) -> ReaderUpgradeStatusStatus:
    if value in READER_UPGRADE_STATUS_STATUS_VALUES:
        return cast(ReaderUpgradeStatusStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_UPGRADE_STATUS_STATUS_VALUES!r}")
