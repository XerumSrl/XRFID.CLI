from typing import Literal, cast

ReaderInterfaceConnectionStatusDataItemConnectionStatus = Literal['Connected', 'disconnected']

READER_INTERFACE_CONNECTION_STATUS_DATA_ITEM_CONNECTION_STATUS_VALUES: set[ReaderInterfaceConnectionStatusDataItemConnectionStatus] = { 'Connected', 'disconnected',  }

def check_reader_interface_connection_status_data_item_connection_status(value: str) -> ReaderInterfaceConnectionStatusDataItemConnectionStatus:
    if value in READER_INTERFACE_CONNECTION_STATUS_DATA_ITEM_CONNECTION_STATUS_VALUES:
        return cast(ReaderInterfaceConnectionStatusDataItemConnectionStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_INTERFACE_CONNECTION_STATUS_DATA_ITEM_CONNECTION_STATUS_VALUES!r}")
