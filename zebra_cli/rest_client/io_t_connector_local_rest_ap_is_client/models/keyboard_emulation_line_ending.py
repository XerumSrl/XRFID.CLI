from typing import Literal, cast

KeyboardEmulationLineEnding = Literal['CR', 'CRLF', 'LF', 'NONE']

KEYBOARD_EMULATION_LINE_ENDING_VALUES: set[KeyboardEmulationLineEnding] = { 'CR', 'CRLF', 'LF', 'NONE',  }

def check_keyboard_emulation_line_ending(value: str) -> KeyboardEmulationLineEnding:
    if value in KEYBOARD_EMULATION_LINE_ENDING_VALUES:
        return cast(KeyboardEmulationLineEnding, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {KEYBOARD_EMULATION_LINE_ENDING_VALUES!r}")
