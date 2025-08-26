from typing import Literal, cast

TagIdFilterOperation = Literal['exclude', 'include']

TAG_ID_FILTER_OPERATION_VALUES: set[TagIdFilterOperation] = { 'exclude', 'include',  }

def check_tag_id_filter_operation(value: str) -> TagIdFilterOperation:
    if value in TAG_ID_FILTER_OPERATION_VALUES:
        return cast(TagIdFilterOperation, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TAG_ID_FILTER_OPERATION_VALUES!r}")
