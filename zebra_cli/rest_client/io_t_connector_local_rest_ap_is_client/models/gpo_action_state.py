from typing import Literal, cast

GPOActionState = Literal['HIGH', 'LOW']

GPO_ACTION_STATE_VALUES: set[GPOActionState] = { 'HIGH', 'LOW',  }

def check_gpo_action_state(value: str) -> GPOActionState:
    if value in GPO_ACTION_STATE_VALUES:
        return cast(GPOActionState, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPO_ACTION_STATE_VALUES!r}")
