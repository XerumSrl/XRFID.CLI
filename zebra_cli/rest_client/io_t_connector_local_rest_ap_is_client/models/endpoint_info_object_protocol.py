from typing import Literal, cast

EndpointInfoObjectProtocol = Literal['ssl', 'tcp', 'ws', 'wss']

ENDPOINT_INFO_OBJECT_PROTOCOL_VALUES: set[EndpointInfoObjectProtocol] = { 'ssl', 'tcp', 'ws', 'wss',  }

def check_endpoint_info_object_protocol(value: str) -> EndpointInfoObjectProtocol:
    if value in ENDPOINT_INFO_OBJECT_PROTOCOL_VALUES:
        return cast(EndpointInfoObjectProtocol, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ENDPOINT_INFO_OBJECT_PROTOCOL_VALUES!r}")
