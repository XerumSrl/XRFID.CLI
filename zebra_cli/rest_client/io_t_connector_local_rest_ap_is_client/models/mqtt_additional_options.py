from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MQTTAdditionalOptions")



@_attrs_define
class MQTTAdditionalOptions:
    """ Configuration of Additional MQTT Options

        Attributes:
            keep_alive (int): The duration (in seconds) to buffer messages when the connection to MQTT is lost
            clean_session (bool): Enables or Disables cleaning session of connection to MQTT
            debug (bool): Enables or Disables logging of MQTT Debug messages
            reconnect_delay (int): The period to attempt reconnection when MQTT connection is lost (in seconds)
            reconnect_delay_max (int): Maximum amount of time (in seconds) to attempt to reconnect after MQTT connection is
                lost (0 indicates continuing to try "forever")
            client_id (str): Identifier for the MQTT client
            qos (int): Sets the Quality of Service for the MQTT Connection
            retain (Union[Unset, bool]): stores the latest message on a topic, delivering it to any new subscribers
                immediately upon connection. Default: False.
     """

    keep_alive: int
    clean_session: bool
    debug: bool
    reconnect_delay: int
    reconnect_delay_max: int
    client_id: str
    qos: int
    retain: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        keep_alive = self.keep_alive

        clean_session = self.clean_session

        debug = self.debug

        reconnect_delay = self.reconnect_delay

        reconnect_delay_max = self.reconnect_delay_max

        client_id = self.client_id

        qos = self.qos

        retain = self.retain


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "keepAlive": keep_alive,
            "cleanSession": clean_session,
            "debug": debug,
            "reconnectDelay": reconnect_delay,
            "reconnectDelayMax": reconnect_delay_max,
            "clientId": client_id,
            "qos": qos,
        })
        if retain is not UNSET:
            field_dict["retain"] = retain

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keep_alive = d.pop("keepAlive")

        clean_session = d.pop("cleanSession")

        debug = d.pop("debug")

        reconnect_delay = d.pop("reconnectDelay")

        reconnect_delay_max = d.pop("reconnectDelayMax")

        client_id = d.pop("clientId")

        qos = d.pop("qos")

        retain = d.pop("retain", UNSET)

        mqtt_additional_options = cls(
            keep_alive=keep_alive,
            clean_session=clean_session,
            debug=debug,
            reconnect_delay=reconnect_delay,
            reconnect_delay_max=reconnect_delay_max,
            client_id=client_id,
            qos=qos,
            retain=retain,
        )


        mqtt_additional_options.additional_properties = d
        return mqtt_additional_options

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
