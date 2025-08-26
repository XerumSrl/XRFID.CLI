from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.azure_additional_qos import AZUREAdditionalQos
from ..models.azure_additional_qos import check_azure_additional_qos
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="AZUREAdditional")



@_attrs_define
class AZUREAdditional:
    """ 
        Attributes:
            keep_alive (Union[Unset, int]): Keep alive duration
            clean_session (Union[Unset, bool]): Enable or Disable clean session
            reconnect_delay (Union[Unset, int]): Reconnect Delay in seconds
            reconnect_delay_max (Union[Unset, int]): Maximum reconnection delay in seconds
            client_id (Union[Unset, str]): Client Id
            debug (Union[Unset, bool]): Enable or Disable debug mode
            qos (Union[Unset, AZUREAdditionalQos]): QOS level
     """

    keep_alive: Union[Unset, int] = UNSET
    clean_session: Union[Unset, bool] = UNSET
    reconnect_delay: Union[Unset, int] = UNSET
    reconnect_delay_max: Union[Unset, int] = UNSET
    client_id: Union[Unset, str] = UNSET
    debug: Union[Unset, bool] = UNSET
    qos: Union[Unset, AZUREAdditionalQos] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        keep_alive = self.keep_alive

        clean_session = self.clean_session

        reconnect_delay = self.reconnect_delay

        reconnect_delay_max = self.reconnect_delay_max

        client_id = self.client_id

        debug = self.debug

        qos: Union[Unset, int] = UNSET
        if not isinstance(self.qos, Unset):
            qos = self.qos



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if keep_alive is not UNSET:
            field_dict["keepAlive"] = keep_alive
        if clean_session is not UNSET:
            field_dict["cleanSession"] = clean_session
        if reconnect_delay is not UNSET:
            field_dict["reconnectDelay"] = reconnect_delay
        if reconnect_delay_max is not UNSET:
            field_dict["reconnectDelayMax"] = reconnect_delay_max
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if debug is not UNSET:
            field_dict["debug"] = debug
        if qos is not UNSET:
            field_dict["qos"] = qos

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keep_alive = d.pop("keepAlive", UNSET)

        clean_session = d.pop("cleanSession", UNSET)

        reconnect_delay = d.pop("reconnectDelay", UNSET)

        reconnect_delay_max = d.pop("reconnectDelayMax", UNSET)

        client_id = d.pop("clientId", UNSET)

        debug = d.pop("debug", UNSET)

        _qos = d.pop("qos", UNSET)
        qos: Union[Unset, AZUREAdditionalQos]
        if isinstance(_qos,  Unset):
            qos = UNSET
        else:
            qos = check_azure_additional_qos(_qos)




        azure_additional = cls(
            keep_alive=keep_alive,
            clean_session=clean_session,
            reconnect_delay=reconnect_delay,
            reconnect_delay_max=reconnect_delay_max,
            client_id=client_id,
            debug=debug,
            qos=qos,
        )


        azure_additional.additional_properties = d
        return azure_additional

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
