from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lock_config_actions_item import check_lock_config_actions_item
from ..models.lock_config_actions_item import LockConfigActionsItem
from typing import cast






T = TypeVar("T", bound="LockConfig")



@_attrs_define
class LockConfig:
    """ 
        Attributes:
            actions (list[LockConfigActionsItem]): Payload Field (see EPC Gen2 Spec)
     """

    actions: list[LockConfigActionsItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        actions = []
        for actions_item_data in self.actions:
            actions_item: str = actions_item_data
            actions.append(actions_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "actions": actions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in (_actions):
            actions_item = check_lock_config_actions_item(actions_item_data)



            actions.append(actions_item)


        lock_config = cls(
            actions=actions,
        )


        lock_config.additional_properties = d
        return lock_config

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
