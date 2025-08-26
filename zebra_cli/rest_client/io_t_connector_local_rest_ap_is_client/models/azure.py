from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.azure_additional import AZUREAdditional
  from ..models.azure_endpoint import AZUREEndpoint
  from ..models.azure_basic_authentication import AZUREBasicAuthentication
  from ..models.azure_security import AZURESecurity





T = TypeVar("T", bound="AZURE")



@_attrs_define
class AZURE:
    """ Configuration of AZURE server

        Attributes:
            endpoint (AZUREEndpoint): Enable or Disable Security
            additional (Union[Unset, AZUREAdditional]):
            basic_authentication (Union[Unset, AZUREBasicAuthentication]):
            subscribe_topic (Union[Unset, list[str]]): List of topics to subscribe to
            publish_topic (Union[Unset, list[str]]): List of topics to publish to
            enable_security (Union[Unset, bool]): Enable or Disable security
            security (Union[Unset, AZURESecurity]):
     """

    endpoint: 'AZUREEndpoint'
    additional: Union[Unset, 'AZUREAdditional'] = UNSET
    basic_authentication: Union[Unset, 'AZUREBasicAuthentication'] = UNSET
    subscribe_topic: Union[Unset, list[str]] = UNSET
    publish_topic: Union[Unset, list[str]] = UNSET
    enable_security: Union[Unset, bool] = UNSET
    security: Union[Unset, 'AZURESecurity'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.azure_additional import AZUREAdditional
        from ..models.azure_endpoint import AZUREEndpoint
        from ..models.azure_basic_authentication import AZUREBasicAuthentication
        from ..models.azure_security import AZURESecurity
        endpoint = self.endpoint.to_dict()

        additional: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.additional, Unset):
            additional = self.additional.to_dict()

        basic_authentication: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.basic_authentication, Unset):
            basic_authentication = self.basic_authentication.to_dict()

        subscribe_topic: Union[Unset, list[str]] = UNSET
        if not isinstance(self.subscribe_topic, Unset):
            subscribe_topic = self.subscribe_topic



        publish_topic: Union[Unset, list[str]] = UNSET
        if not isinstance(self.publish_topic, Unset):
            publish_topic = self.publish_topic



        enable_security = self.enable_security

        security: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.security, Unset):
            security = self.security.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "endpoint": endpoint,
        })
        if additional is not UNSET:
            field_dict["additional"] = additional
        if basic_authentication is not UNSET:
            field_dict["basicAuthentication"] = basic_authentication
        if subscribe_topic is not UNSET:
            field_dict["subscribeTopic"] = subscribe_topic
        if publish_topic is not UNSET:
            field_dict["publishTopic"] = publish_topic
        if enable_security is not UNSET:
            field_dict["enableSecurity"] = enable_security
        if security is not UNSET:
            field_dict["security"] = security

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.azure_additional import AZUREAdditional
        from ..models.azure_endpoint import AZUREEndpoint
        from ..models.azure_basic_authentication import AZUREBasicAuthentication
        from ..models.azure_security import AZURESecurity
        d = dict(src_dict)
        endpoint = AZUREEndpoint.from_dict(d.pop("endpoint"))




        _additional = d.pop("additional", UNSET)
        additional: Union[Unset, AZUREAdditional]
        if isinstance(_additional,  Unset):
            additional = UNSET
        else:
            additional = AZUREAdditional.from_dict(_additional)




        _basic_authentication = d.pop("basicAuthentication", UNSET)
        basic_authentication: Union[Unset, AZUREBasicAuthentication]
        if isinstance(_basic_authentication,  Unset):
            basic_authentication = UNSET
        else:
            basic_authentication = AZUREBasicAuthentication.from_dict(_basic_authentication)




        subscribe_topic = cast(list[str], d.pop("subscribeTopic", UNSET))


        publish_topic = cast(list[str], d.pop("publishTopic", UNSET))


        enable_security = d.pop("enableSecurity", UNSET)

        _security = d.pop("security", UNSET)
        security: Union[Unset, AZURESecurity]
        if isinstance(_security,  Unset):
            security = UNSET
        else:
            security = AZURESecurity.from_dict(_security)




        azure = cls(
            endpoint=endpoint,
            additional=additional,
            basic_authentication=basic_authentication,
            subscribe_topic=subscribe_topic,
            publish_topic=publish_topic,
            enable_security=enable_security,
            security=security,
        )


        azure.additional_properties = d
        return azure

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
