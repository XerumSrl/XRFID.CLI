from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.log_level_components_item import LogLevelComponentsItem





T = TypeVar("T", bound="LogLevel")



@_attrs_define
class LogLevel:
    """ Reader Logging Configuration

        Attributes:
            radio_packet_log (Union[Unset, bool]): Enables or Disables the Radio Control radio packet log
            components (Union[Unset, list['LogLevelComponentsItem']]): System sub-components
     """

    radio_packet_log: Union[Unset, bool] = UNSET
    components: Union[Unset, list['LogLevelComponentsItem']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_level_components_item import LogLevelComponentsItem
        radio_packet_log = self.radio_packet_log

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if radio_packet_log is not UNSET:
            field_dict["radioPacketLog"] = radio_packet_log
        if components is not UNSET:
            field_dict["components"] = components

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_level_components_item import LogLevelComponentsItem
        d = dict(src_dict)
        radio_packet_log = d.pop("radioPacketLog", UNSET)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in (_components or []):
            components_item = LogLevelComponentsItem.from_dict(components_item_data)



            components.append(components_item)


        log_level = cls(
            radio_packet_log=radio_packet_log,
            components=components,
        )


        log_level.additional_properties = d
        return log_level

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
