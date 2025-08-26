from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.keyboard_emulation_line_ending import check_keyboard_emulation_line_ending
from ..models.keyboard_emulation_line_ending import KeyboardEmulationLineEnding
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.keyboard_emulation_additional_config import KeyboardEmulationAdditionalConfig





T = TypeVar("T", bound="KeyboardEmulation")



@_attrs_define
class KeyboardEmulation:
    """ Configuration of Keyboard Emulation

        Attributes:
            key_stroke_delay_in_ms (int): Key Stroke Delay in milliseconds
            line_ending (KeyboardEmulationLineEnding): Format Line endings
            additional_config (Union[Unset, KeyboardEmulationAdditionalConfig]):
     """

    key_stroke_delay_in_ms: int
    line_ending: KeyboardEmulationLineEnding
    additional_config: Union[Unset, 'KeyboardEmulationAdditionalConfig'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.keyboard_emulation_additional_config import KeyboardEmulationAdditionalConfig
        key_stroke_delay_in_ms = self.key_stroke_delay_in_ms

        line_ending: str = self.line_ending

        additional_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.additional_config, Unset):
            additional_config = self.additional_config.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "keyStrokeDelayInMs": key_stroke_delay_in_ms,
            "lineEnding": line_ending,
        })
        if additional_config is not UNSET:
            field_dict["additionalConfig"] = additional_config

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.keyboard_emulation_additional_config import KeyboardEmulationAdditionalConfig
        d = dict(src_dict)
        key_stroke_delay_in_ms = d.pop("keyStrokeDelayInMs")

        line_ending = check_keyboard_emulation_line_ending(d.pop("lineEnding"))




        _additional_config = d.pop("additionalConfig", UNSET)
        additional_config: Union[Unset, KeyboardEmulationAdditionalConfig]
        if isinstance(_additional_config,  Unset):
            additional_config = UNSET
        else:
            additional_config = KeyboardEmulationAdditionalConfig.from_dict(_additional_config)




        keyboard_emulation = cls(
            key_stroke_delay_in_ms=key_stroke_delay_in_ms,
            line_ending=line_ending,
            additional_config=additional_config,
        )


        keyboard_emulation.additional_properties = d
        return keyboard_emulation

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
