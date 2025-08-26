from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.mqtt_security import MQTTSecurity
  from ..models.endpoint_info_object import EndpointInfoObject
  from ..models.basic_authentication_for_external_server_connections import BasicAuthenticationForExternalServerConnections
  from ..models.mqtt_additional_options import MQTTAdditionalOptions





T = TypeVar("T", bound="MQTT")



@_attrs_define
class MQTT:
    """ Configuration of MQTT

        Attributes:
            endpoint (Union['EndpointInfoObject', str]): Configuration of MQTT Endpoint
            enable_security (bool): Enable or Disable Security for MQTT connection
            additional (MQTTAdditionalOptions): Configuration of Additional MQTT Options
            publish_topic (list[str]): Topic to which to publish messages
            security (Union[Unset, MQTTSecurity]): Configuration of MQTT Security
            basic_authentication (Union[Unset, BasicAuthenticationForExternalServerConnections]): Configuration of Basic
                Authentication
            subscribe_topic (Union[Unset, list[str]]): Topic to which to subscribe for messages
     """

    endpoint: Union['EndpointInfoObject', str]
    enable_security: bool
    additional: 'MQTTAdditionalOptions'
    publish_topic: list[str]
    security: Union[Unset, 'MQTTSecurity'] = UNSET
    basic_authentication: Union[Unset, 'BasicAuthenticationForExternalServerConnections'] = UNSET
    subscribe_topic: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.mqtt_security import MQTTSecurity
        from ..models.endpoint_info_object import EndpointInfoObject
        from ..models.basic_authentication_for_external_server_connections import BasicAuthenticationForExternalServerConnections
        from ..models.mqtt_additional_options import MQTTAdditionalOptions
        endpoint: Union[dict[str, Any], str]
        if isinstance(self.endpoint, EndpointInfoObject):
            endpoint = self.endpoint.to_dict()
        else:
            endpoint = self.endpoint

        enable_security = self.enable_security

        additional = self.additional.to_dict()

        publish_topic = self.publish_topic



        security: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.security, Unset):
            security = self.security.to_dict()

        basic_authentication: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.basic_authentication, Unset):
            basic_authentication = self.basic_authentication.to_dict()

        subscribe_topic: Union[Unset, list[str]] = UNSET
        if not isinstance(self.subscribe_topic, Unset):
            subscribe_topic = self.subscribe_topic




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "endpoint": endpoint,
            "enableSecurity": enable_security,
            "additional": additional,
            "publishTopic": publish_topic,
        })
        if security is not UNSET:
            field_dict["security"] = security
        if basic_authentication is not UNSET:
            field_dict["basicAuthentication"] = basic_authentication
        if subscribe_topic is not UNSET:
            field_dict["subscribeTopic"] = subscribe_topic

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mqtt_security import MQTTSecurity
        from ..models.endpoint_info_object import EndpointInfoObject
        from ..models.basic_authentication_for_external_server_connections import BasicAuthenticationForExternalServerConnections
        from ..models.mqtt_additional_options import MQTTAdditionalOptions
        d = dict(src_dict)
        def _parse_endpoint(data: object) -> Union['EndpointInfoObject', str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasmqtt_endpoint_v_1_type_0 = EndpointInfoObject.from_dict(data)



                return componentsschemasmqtt_endpoint_v_1_type_0
            except: # noqa: E722
                pass
            return cast(Union['EndpointInfoObject', str], data)

        endpoint = _parse_endpoint(d.pop("endpoint"))


        enable_security = d.pop("enableSecurity")

        additional = MQTTAdditionalOptions.from_dict(d.pop("additional"))




        publish_topic = cast(list[str], d.pop("publishTopic"))


        _security = d.pop("security", UNSET)
        security: Union[Unset, MQTTSecurity]
        if isinstance(_security,  Unset):
            security = UNSET
        else:
            security = MQTTSecurity.from_dict(_security)




        _basic_authentication = d.pop("basicAuthentication", UNSET)
        basic_authentication: Union[Unset, BasicAuthenticationForExternalServerConnections]
        if isinstance(_basic_authentication,  Unset):
            basic_authentication = UNSET
        else:
            basic_authentication = BasicAuthenticationForExternalServerConnections.from_dict(_basic_authentication)




        subscribe_topic = cast(list[str], d.pop("subscribeTopic", UNSET))


        mqtt = cls(
            endpoint=endpoint,
            enable_security=enable_security,
            additional=additional,
            publish_topic=publish_topic,
            security=security,
            basic_authentication=basic_authentication,
            subscribe_topic=subscribe_topic,
        )


        mqtt.additional_properties = d
        return mqtt

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
