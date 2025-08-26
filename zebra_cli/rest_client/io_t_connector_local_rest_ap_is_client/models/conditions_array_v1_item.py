from typing import Literal, cast

ConditionsArrayV1Item = Literal['IS_CLOUD_CONNECTED', 'IS_RADIO_ONGOING', '~IS_CLOUD_CONNECTED', '~IS_RADIO_ONGOING']

CONDITIONS_ARRAY_V1_ITEM_VALUES: set[ConditionsArrayV1Item] = { 'IS_CLOUD_CONNECTED', 'IS_RADIO_ONGOING', '~IS_CLOUD_CONNECTED', '~IS_RADIO_ONGOING',  }

def check_conditions_array_v1_item(value: str) -> ConditionsArrayV1Item:
    if value in CONDITIONS_ARRAY_V1_ITEM_VALUES:
        return cast(ConditionsArrayV1Item, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CONDITIONS_ARRAY_V1_ITEM_VALUES!r}")
