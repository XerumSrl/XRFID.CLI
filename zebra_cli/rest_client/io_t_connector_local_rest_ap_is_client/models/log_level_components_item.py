from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_level_components_item_component_name import check_log_level_components_item_component_name
from ..models.log_level_components_item_component_name import LogLevelComponentsItemComponentName
from ..models.log_level_components_item_level import check_log_level_components_item_level
from ..models.log_level_components_item_level import LogLevelComponentsItemLevel
from typing import cast






T = TypeVar("T", bound="LogLevelComponentsItem")



@_attrs_define
class LogLevelComponentsItem:
    """ 
        Attributes:
            component_name (LogLevelComponentsItemComponentName): Name of subcomponent
            level (LogLevelComponentsItemLevel): Logging Level
     """

    component_name: LogLevelComponentsItemComponentName
    level: LogLevelComponentsItemLevel
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        component_name: str = self.component_name

        level: str = self.level


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "componentName": component_name,
            "level": level,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        component_name = check_log_level_components_item_component_name(d.pop("componentName"))




        level = check_log_level_components_item_level(d.pop("level"))




        log_level_components_item = cls(
            component_name=component_name,
            level=level,
        )


        log_level_components_item.additional_properties = d
        return log_level_components_item

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
