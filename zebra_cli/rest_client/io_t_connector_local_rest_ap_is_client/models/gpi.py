from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.gpi_signal import check_gpi_signal
from ..models.gpi_signal import GpiSignal
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="Gpi")



@_attrs_define
class Gpi:
    """ 
        Attributes:
            port (int): GPI Port Number
            signal (GpiSignal): Transition to this GPI will trigger event
            debounce_time (Union[Unset, int]): Time (in milliseconds) until GPI must remain at signal level to trigger event
                Default: 0.
     """

    port: int
    signal: GpiSignal
    debounce_time: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        port = self.port

        signal: str = self.signal

        debounce_time = self.debounce_time


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "port": port,
            "signal": signal,
        })
        if debounce_time is not UNSET:
            field_dict["debounceTime"] = debounce_time

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        port = d.pop("port")

        signal = check_gpi_signal(d.pop("signal"))




        debounce_time = d.pop("debounceTime", UNSET)

        gpi = cls(
            port=port,
            signal=signal,
            debounce_time=debounce_time,
        )


        gpi.additional_properties = d
        return gpi

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
