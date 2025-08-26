from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.tag_data_events_batching_configuration import TagDataEventsBatchingConfiguration
  from ..models.tag_data_events_retention_configuration import TagDataEventsRetentionConfiguration





T = TypeVar("T", bound="EventConnectionsItemAdditionalOptions")



@_attrs_define
class EventConnectionsItemAdditionalOptions:
    """ additional configuration options

        Attributes:
            batching (Union[Unset, TagDataEventsBatchingConfiguration]): Tag Data Events batching configuration
            retention (Union[Unset, TagDataEventsRetentionConfiguration]): Tag Data Events Retention Configuration on
                connection lost
     """

    batching: Union[Unset, 'TagDataEventsBatchingConfiguration'] = UNSET
    retention: Union[Unset, 'TagDataEventsRetentionConfiguration'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.tag_data_events_batching_configuration import TagDataEventsBatchingConfiguration
        from ..models.tag_data_events_retention_configuration import TagDataEventsRetentionConfiguration
        batching: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.batching, Unset):
            batching = self.batching.to_dict()

        retention: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.retention, Unset):
            retention = self.retention.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if batching is not UNSET:
            field_dict["batching"] = batching
        if retention is not UNSET:
            field_dict["retention"] = retention

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tag_data_events_batching_configuration import TagDataEventsBatchingConfiguration
        from ..models.tag_data_events_retention_configuration import TagDataEventsRetentionConfiguration
        d = dict(src_dict)
        _batching = d.pop("batching", UNSET)
        batching: Union[Unset, TagDataEventsBatchingConfiguration]
        if isinstance(_batching,  Unset):
            batching = UNSET
        else:
            batching = TagDataEventsBatchingConfiguration.from_dict(_batching)




        _retention = d.pop("retention", UNSET)
        retention: Union[Unset, TagDataEventsRetentionConfiguration]
        if isinstance(_retention,  Unset):
            retention = UNSET
        else:
            retention = TagDataEventsRetentionConfiguration.from_dict(_retention)




        event_connections_item_additional_options = cls(
            batching=batching,
            retention=retention,
        )


        event_connections_item_additional_options.additional_properties = d
        return event_connections_item_additional_options

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
