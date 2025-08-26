from typing import Literal, cast

ActionConditionsV1Type1Operator = Literal['and', 'or']

ACTION_CONDITIONS_V1_TYPE_1_OPERATOR_VALUES: set[ActionConditionsV1Type1Operator] = { 'and', 'or',  }

def check_action_conditions_v1_type_1_operator(value: str) -> ActionConditionsV1Type1Operator:
    if value in ACTION_CONDITIONS_V1_TYPE_1_OPERATOR_VALUES:
        return cast(ActionConditionsV1Type1Operator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ACTION_CONDITIONS_V1_TYPE_1_OPERATOR_VALUES!r}")
