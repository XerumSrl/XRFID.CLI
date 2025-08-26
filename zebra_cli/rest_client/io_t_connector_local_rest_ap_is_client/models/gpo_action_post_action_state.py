from typing import Literal, cast

GPOActionPostActionState = Literal['HIGH', 'LOW']

GPO_ACTION_POST_ACTION_STATE_VALUES: set[GPOActionPostActionState] = { 'HIGH', 'LOW',  }

def check_gpo_action_post_action_state(value: str) -> GPOActionPostActionState:
    if value in GPO_ACTION_POST_ACTION_STATE_VALUES:
        return cast(GPOActionPostActionState, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPO_ACTION_POST_ACTION_STATE_VALUES!r}")
