from typing import Literal, cast

TagMetaDataV1Item = Literal['ANTENNA', 'CHANNEL', 'CRC', 'EPC', 'HOSTNAME', 'MAC', 'PC', 'PHASE', 'RSSI', 'SEEN_COUNT', 'TID', 'USER', 'XPC']

TAG_META_DATA_V1_ITEM_VALUES: set[TagMetaDataV1Item] = { 'ANTENNA', 'CHANNEL', 'CRC', 'EPC', 'HOSTNAME', 'MAC', 'PC', 'PHASE', 'RSSI', 'SEEN_COUNT', 'TID', 'USER', 'XPC',  }

def check_tag_meta_data_v1_item(value: str) -> TagMetaDataV1Item:
    if value in TAG_META_DATA_V1_ITEM_VALUES:
        return cast(TagMetaDataV1Item, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TAG_META_DATA_V1_ITEM_VALUES!r}")
