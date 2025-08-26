from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.event_connections_item_type import check_event_connections_item_type
from ..models.event_connections_item_type import EventConnectionsItemType
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.azure import AZURE
  from ..models.http_post import HTTPPost
  from ..models.websocket import Websocket
  from ..models.event_connections_item_additional_options import EventConnectionsItemAdditionalOptions
  from ..models.keyboard_emulation import KeyboardEmulation
  from ..models.mqtt import MQTT
  from ..models.aws import AWS
  from ..models.tcpip import TCPIP





T = TypeVar("T", bound="EventConnectionsItem")



@_attrs_define
class EventConnectionsItem:
    """ 
        Attributes:
            type_ (Union[Unset, EventConnectionsItemType]): Type of Channel Example: mqtt.
            options (Union['AWS', 'AZURE', 'HTTPPost', 'KeyboardEmulation', 'MQTT', 'TCPIP', 'Websocket', Unset]): Options
                for the chosen type
            name (Union[Unset, str]): name of endpoint
            description (Union[Unset, str]): description of endpoint
            additional_options (Union[Unset, EventConnectionsItemAdditionalOptions]): additional configuration options
     """

    type_: Union[Unset, EventConnectionsItemType] = UNSET
    options: Union['AWS', 'AZURE', 'HTTPPost', 'KeyboardEmulation', 'MQTT', 'TCPIP', 'Websocket', Unset] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_options: Union[Unset, 'EventConnectionsItemAdditionalOptions'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.azure import AZURE
        from ..models.http_post import HTTPPost
        from ..models.websocket import Websocket
        from ..models.event_connections_item_additional_options import EventConnectionsItemAdditionalOptions
        from ..models.keyboard_emulation import KeyboardEmulation
        from ..models.mqtt import MQTT
        from ..models.aws import AWS
        from ..models.tcpip import TCPIP
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_


        options: Union[Unset, dict[str, Any]]
        if isinstance(self.options, Unset):
            options = UNSET
        elif isinstance(self.options, MQTT):
            options = self.options.to_dict()
        elif isinstance(self.options, HTTPPost):
            options = self.options.to_dict()
        elif isinstance(self.options, TCPIP):
            options = self.options.to_dict()
        elif isinstance(self.options, Websocket):
            options = self.options.to_dict()
        elif isinstance(self.options, KeyboardEmulation):
            options = self.options.to_dict()
        elif isinstance(self.options, AZURE):
            options = self.options.to_dict()
        else:
            options = self.options.to_dict()


        name = self.name

        description = self.description

        additional_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.additional_options, Unset):
            additional_options = self.additional_options.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if options is not UNSET:
            field_dict["options"] = options
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if additional_options is not UNSET:
            field_dict["additionalOptions"] = additional_options

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.azure import AZURE
        from ..models.http_post import HTTPPost
        from ..models.websocket import Websocket
        from ..models.event_connections_item_additional_options import EventConnectionsItemAdditionalOptions
        from ..models.keyboard_emulation import KeyboardEmulation
        from ..models.mqtt import MQTT
        from ..models.aws import AWS
        from ..models.tcpip import TCPIP
        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, EventConnectionsItemType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = check_event_connections_item_type(_type_)




        def _parse_options(data: object) -> Union['AWS', 'AZURE', 'HTTPPost', 'KeyboardEmulation', 'MQTT', 'TCPIP', 'Websocket', Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_0 = MQTT.from_dict(data)



                return options_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_1 = HTTPPost.from_dict(data)



                return options_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_2 = TCPIP.from_dict(data)



                return options_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_3 = Websocket.from_dict(data)



                return options_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_4 = KeyboardEmulation.from_dict(data)



                return options_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                options_type_5 = AZURE.from_dict(data)



                return options_type_5
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            options_type_6 = AWS.from_dict(data)



            return options_type_6

        options = _parse_options(d.pop("options", UNSET))


        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _additional_options = d.pop("additionalOptions", UNSET)
        additional_options: Union[Unset, EventConnectionsItemAdditionalOptions]
        if isinstance(_additional_options,  Unset):
            additional_options = UNSET
        else:
            additional_options = EventConnectionsItemAdditionalOptions.from_dict(_additional_options)




        event_connections_item = cls(
            type_=type_,
            options=options,
            name=name,
            description=description,
            additional_options=additional_options,
        )


        event_connections_item.additional_properties = d
        return event_connections_item

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
