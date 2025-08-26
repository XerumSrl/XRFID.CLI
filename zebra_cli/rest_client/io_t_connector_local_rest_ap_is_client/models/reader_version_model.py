from typing import Literal, cast

ReaderVersionModel = Literal['ATR7000', 'FX7500', 'FX9600']

READER_VERSION_MODEL_VALUES: set[ReaderVersionModel] = { 'ATR7000', 'FX7500', 'FX9600',  }

def check_reader_version_model(value: str) -> ReaderVersionModel:
    if value in READER_VERSION_MODEL_VALUES:
        return cast(ReaderVersionModel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_VERSION_MODEL_VALUES!r}")
