from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.delay_between_antenna_cycles_type import check_delay_between_antenna_cycles_type
from ..models.delay_between_antenna_cycles_type import DelayBetweenAntennaCyclesType
from typing import cast






T = TypeVar("T", bound="DelayBetweenAntennaCycles")



@_attrs_define
class DelayBetweenAntennaCycles:
    """ This introduces a delay between antenna cycles if no tags are read or if no unique tags are read. This allows the
    reader to share the spectrum if there are no tags to be read.

    If absent,
    on the ATR7000 and the FX9600, delayBetweenAntennas cycles is set to wait for 75 mS if no unique tags are read
    during a antenna cycle.
    on the FX7500, delayBetweenAntennas cycles is set to wait for 75 mS if no tags are read during a antenna cycle.

        Attributes:
            type_ (DelayBetweenAntennaCyclesType): Condition under which to delay between antenna cycles
            duration (int): Delay between antennas cycles in milliseconds to wait. Will only wait if the type (no tags or no
                unique tags) is met. If the type is DISABLED, duration must to be set to 0. IF the type is no DISABLED< the
                value must be set to a non-zero value.
     """

    type_: DelayBetweenAntennaCyclesType
    duration: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        duration = self.duration


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "duration": duration,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_delay_between_antenna_cycles_type(d.pop("type"))




        duration = d.pop("duration")

        delay_between_antenna_cycles = cls(
            type_=type_,
            duration=duration,
        )


        delay_between_antenna_cycles.additional_properties = d
        return delay_between_antenna_cycles

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
