from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="Start")



@_attrs_define
class Start:
    """ Start tag reads

        Attributes:
            do_not_persist_state (Union[Unset, bool]): persist current tag read state of reader Default: True.
     """

    do_not_persist_state: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        do_not_persist_state = self.do_not_persist_state


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if do_not_persist_state is not UNSET:
            field_dict["doNotPersistState"] = do_not_persist_state

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        do_not_persist_state = d.pop("doNotPersistState", UNSET)

        start = cls(
            do_not_persist_state=do_not_persist_state,
        )


        start.additional_properties = d
        return start

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
