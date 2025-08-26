from typing import Literal, cast

TagIdFilterMatch = Literal['prefix', 'regex', 'suffix']

TAG_ID_FILTER_MATCH_VALUES: set[TagIdFilterMatch] = { 'prefix', 'regex', 'suffix',  }

def check_tag_id_filter_match(value: str) -> TagIdFilterMatch:
    if value in TAG_ID_FILTER_MATCH_VALUES:
        return cast(TagIdFilterMatch, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TAG_ID_FILTER_MATCH_VALUES!r}")
