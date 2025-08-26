from typing import Literal, cast

GPOActionType = Literal['GPO']

GPO_ACTION_TYPE_VALUES: set[GPOActionType] = { 'GPO',  }

def check_gpo_action_type(value: str) -> GPOActionType:
    if value in GPO_ACTION_TYPE_VALUES:
        return cast(GPOActionType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPO_ACTION_TYPE_VALUES!r}")
