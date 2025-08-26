from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.management_events_configuration_heartbeat_fields_radio_control_item import check_management_events_configuration_heartbeat_fields_radio_control_item
from ..models.management_events_configuration_heartbeat_fields_radio_control_item import ManagementEventsConfigurationHeartbeatFieldsRadioControlItem
from ..models.management_events_configuration_heartbeat_fields_reader_gateway_item import check_management_events_configuration_heartbeat_fields_reader_gateway_item
from ..models.management_events_configuration_heartbeat_fields_reader_gateway_item import ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem
from ..models.management_events_configuration_heartbeat_fields_system_item import check_management_events_configuration_heartbeat_fields_system_item
from ..models.management_events_configuration_heartbeat_fields_system_item import ManagementEventsConfigurationHeartbeatFieldsSystemItem
from ..models.management_events_configuration_heartbeat_fields_userapps_item import check_management_events_configuration_heartbeat_fields_userapps_item
from ..models.management_events_configuration_heartbeat_fields_userapps_item import ManagementEventsConfigurationHeartbeatFieldsUserappsItem
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.management_events_configuration_heartbeat_fields_user_defined import ManagementEventsConfigurationHeartbeatFieldsUserDefined





T = TypeVar("T", bound="ManagementEventsConfigurationHeartbeatFields")



@_attrs_define
class ManagementEventsConfigurationHeartbeatFields:
    """ heartbeat fields

        Attributes:
            radio_control (Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsRadioControlItem]]): Radio Control
                related heartbeat events
            reader_gateway (Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem]]):
            system (Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsSystemItem]]):
            userapps (Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsUserappsItem]]):
            user_defined (Union[Unset, ManagementEventsConfigurationHeartbeatFieldsUserDefined]): Custom user defined field
     """

    radio_control: Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsRadioControlItem]] = UNSET
    reader_gateway: Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem]] = UNSET
    system: Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsSystemItem]] = UNSET
    userapps: Union[Unset, list[ManagementEventsConfigurationHeartbeatFieldsUserappsItem]] = UNSET
    user_defined: Union[Unset, 'ManagementEventsConfigurationHeartbeatFieldsUserDefined'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.management_events_configuration_heartbeat_fields_user_defined import ManagementEventsConfigurationHeartbeatFieldsUserDefined
        radio_control: Union[Unset, list[str]] = UNSET
        if not isinstance(self.radio_control, Unset):
            radio_control = []
            for radio_control_item_data in self.radio_control:
                radio_control_item: str = radio_control_item_data
                radio_control.append(radio_control_item)



        reader_gateway: Union[Unset, list[str]] = UNSET
        if not isinstance(self.reader_gateway, Unset):
            reader_gateway = []
            for reader_gateway_item_data in self.reader_gateway:
                reader_gateway_item: str = reader_gateway_item_data
                reader_gateway.append(reader_gateway_item)



        system: Union[Unset, list[str]] = UNSET
        if not isinstance(self.system, Unset):
            system = []
            for system_item_data in self.system:
                system_item: str = system_item_data
                system.append(system_item)



        userapps: Union[Unset, list[str]] = UNSET
        if not isinstance(self.userapps, Unset):
            userapps = []
            for userapps_item_data in self.userapps:
                userapps_item: str = userapps_item_data
                userapps.append(userapps_item)



        user_defined: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_defined, Unset):
            user_defined = self.user_defined.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if radio_control is not UNSET:
            field_dict["radio_control"] = radio_control
        if reader_gateway is not UNSET:
            field_dict["reader_gateway"] = reader_gateway
        if system is not UNSET:
            field_dict["system"] = system
        if userapps is not UNSET:
            field_dict["userapps"] = userapps
        if user_defined is not UNSET:
            field_dict["userDefined"] = user_defined

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.management_events_configuration_heartbeat_fields_user_defined import ManagementEventsConfigurationHeartbeatFieldsUserDefined
        d = dict(src_dict)
        radio_control = []
        _radio_control = d.pop("radio_control", UNSET)
        for radio_control_item_data in (_radio_control or []):
            radio_control_item = check_management_events_configuration_heartbeat_fields_radio_control_item(radio_control_item_data)



            radio_control.append(radio_control_item)


        reader_gateway = []
        _reader_gateway = d.pop("reader_gateway", UNSET)
        for reader_gateway_item_data in (_reader_gateway or []):
            reader_gateway_item = check_management_events_configuration_heartbeat_fields_reader_gateway_item(reader_gateway_item_data)



            reader_gateway.append(reader_gateway_item)


        system = []
        _system = d.pop("system", UNSET)
        for system_item_data in (_system or []):
            system_item = check_management_events_configuration_heartbeat_fields_system_item(system_item_data)



            system.append(system_item)


        userapps = []
        _userapps = d.pop("userapps", UNSET)
        for userapps_item_data in (_userapps or []):
            userapps_item = check_management_events_configuration_heartbeat_fields_userapps_item(userapps_item_data)



            userapps.append(userapps_item)


        _user_defined = d.pop("userDefined", UNSET)
        user_defined: Union[Unset, ManagementEventsConfigurationHeartbeatFieldsUserDefined]
        if isinstance(_user_defined,  Unset):
            user_defined = UNSET
        else:
            user_defined = ManagementEventsConfigurationHeartbeatFieldsUserDefined.from_dict(_user_defined)




        management_events_configuration_heartbeat_fields = cls(
            radio_control=radio_control,
            reader_gateway=reader_gateway,
            system=system,
            userapps=userapps,
            user_defined=user_defined,
        )


        management_events_configuration_heartbeat_fields.additional_properties = d
        return management_events_configuration_heartbeat_fields

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
