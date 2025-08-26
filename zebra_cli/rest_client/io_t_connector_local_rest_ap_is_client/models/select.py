from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.select_action import check_select_action
from ..models.select_action import SelectAction
from ..models.select_membank import check_select_membank
from ..models.select_membank import SelectMembank
from ..models.select_target import check_select_target
from ..models.select_target import SelectTarget
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="Select")



@_attrs_define
class Select:
    """ 
        Attributes:
            target (SelectTarget): Target Field (see EPC Gen2 Spec)
            action (SelectAction): Action Field (see EPC Gen2 Spec)
            membank (SelectMembank): Membank Field (see EPC Gen2 Spec)
            pointer (int): Pointer Field (see EPC Gen2 Spec)
            length (int): Length Field (see EPC Gen2 Spec)
            mask (str): Mask Field (see EPC Gen2 Spec). The value must be a hex string (only values 0-9 and a-f) and must
                have an even number of characters.
            truncate (Union[Unset, int]): Truncate Field (see EPC Gen2 Spec) If absent, truncation is disabled. If non-zero,
                the value indicates the number of bits to expect in the tag response. Default: 0.
     """

    target: SelectTarget
    action: SelectAction
    membank: SelectMembank
    pointer: int
    length: int
    mask: str
    truncate: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        target: str = self.target

        action: str = self.action

        membank: str = self.membank

        pointer = self.pointer

        length = self.length

        mask = self.mask

        truncate = self.truncate


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "target": target,
            "action": action,
            "membank": membank,
            "pointer": pointer,
            "length": length,
            "mask": mask,
        })
        if truncate is not UNSET:
            field_dict["truncate"] = truncate

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target = check_select_target(d.pop("target"))




        action = check_select_action(d.pop("action"))




        membank = check_select_membank(d.pop("membank"))




        pointer = d.pop("pointer")

        length = d.pop("length")

        mask = d.pop("mask")

        truncate = d.pop("truncate", UNSET)

        select = cls(
            target=target,
            action=action,
            membank=membank,
            pointer=pointer,
            length=length,
            mask=mask,
            truncate=truncate,
        )


        select.additional_properties = d
        return select

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
