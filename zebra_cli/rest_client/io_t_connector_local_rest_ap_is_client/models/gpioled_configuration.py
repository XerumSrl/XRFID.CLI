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
  from ..models.gpioled_configuration_gpo_defaults import GPIOLEDConfigurationGPODefaults
  from ..models.gpioled_configuration_led_defaults import GPIOLEDConfigurationLEDDefaults
  from ..models.led_action import LEDAction
  from ..models.gpo_action import GPOAction
  from ..models.gpioled_configuration_gpi_debounce import GPIOLEDConfigurationGPIDebounce





T = TypeVar("T", bound="GPIOLEDConfiguration")



@_attrs_define
class GPIOLEDConfiguration:
    """ GPIO-LED module configuration

    Configure GPO and LED behaviour based on Events generated

    Supported Events:
    1. GPI_1_L: event raised when GPI 1 changed from HIGH to LOW
    2. GPI_1_H: event raised when GPI 1 changed from LOW to HIGH
    3. GPI_2_L: event raised when GPI 2 changed from HIGH to LOW
    4. GPI_2_H: event raised when GPI 2 changed from LOW to HIGH
    5. CLOUD_DISCONNECT: event raised when reader is disconnected from cloud
    6. CLOUD_CONNECT: event raised when reader is connected to cloud
    7. TAG_READ: event raised when a tag is read
    8. RADIO_START: event raised when inventory operation started using START API
    9. RADIO_STOP: event raised when inventory operation stopped using STOP API

        Attributes:
            gpo_defaults (Union[Unset, GPIOLEDConfigurationGPODefaults]): GPO default configurations
            led_defaults (Union[Unset, GPIOLEDConfigurationLEDDefaults]): LED default configurations
            gpi_1_h (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            gpi_1_l (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            gpi_2_h (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            gpi_2_l (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            cloud_disconnect (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions
                will be performed sequentially.
            cloud_connect (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will
                be performed sequentially.
            tag_read (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            radio_start (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            radio_stop (Union[Unset, list[Union['GPOAction', 'LEDAction']]]): Array of GPO or LED actions. Actions will be
                performed sequentially.
            gpi_debounce (Union[Unset, GPIOLEDConfigurationGPIDebounce]): GPI Debounce Configuration
     """

    gpo_defaults: Union[Unset, 'GPIOLEDConfigurationGPODefaults'] = UNSET
    led_defaults: Union[Unset, 'GPIOLEDConfigurationLEDDefaults'] = UNSET
    gpi_1_h: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    gpi_1_l: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    gpi_2_h: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    gpi_2_l: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    cloud_disconnect: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    cloud_connect: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    tag_read: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    radio_start: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    radio_stop: Union[Unset, list[Union['GPOAction', 'LEDAction']]] = UNSET
    gpi_debounce: Union[Unset, 'GPIOLEDConfigurationGPIDebounce'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.gpioled_configuration_gpo_defaults import GPIOLEDConfigurationGPODefaults
        from ..models.gpioled_configuration_led_defaults import GPIOLEDConfigurationLEDDefaults
        from ..models.led_action import LEDAction
        from ..models.gpo_action import GPOAction
        from ..models.gpioled_configuration_gpi_debounce import GPIOLEDConfigurationGPIDebounce
        gpo_defaults: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.gpo_defaults, Unset):
            gpo_defaults = self.gpo_defaults.to_dict()

        led_defaults: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.led_defaults, Unset):
            led_defaults = self.led_defaults.to_dict()

        gpi_1_h: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.gpi_1_h, Unset):
            gpi_1_h = []
            for componentsschemasgpoled_action_v_1_item_data in self.gpi_1_h:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                gpi_1_h.append(componentsschemasgpoled_action_v_1_item)



        gpi_1_l: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.gpi_1_l, Unset):
            gpi_1_l = []
            for componentsschemasgpoled_action_v_1_item_data in self.gpi_1_l:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                gpi_1_l.append(componentsschemasgpoled_action_v_1_item)



        gpi_2_h: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.gpi_2_h, Unset):
            gpi_2_h = []
            for componentsschemasgpoled_action_v_1_item_data in self.gpi_2_h:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                gpi_2_h.append(componentsschemasgpoled_action_v_1_item)



        gpi_2_l: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.gpi_2_l, Unset):
            gpi_2_l = []
            for componentsschemasgpoled_action_v_1_item_data in self.gpi_2_l:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                gpi_2_l.append(componentsschemasgpoled_action_v_1_item)



        cloud_disconnect: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cloud_disconnect, Unset):
            cloud_disconnect = []
            for componentsschemasgpoled_action_v_1_item_data in self.cloud_disconnect:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                cloud_disconnect.append(componentsschemasgpoled_action_v_1_item)



        cloud_connect: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cloud_connect, Unset):
            cloud_connect = []
            for componentsschemasgpoled_action_v_1_item_data in self.cloud_connect:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                cloud_connect.append(componentsschemasgpoled_action_v_1_item)



        tag_read: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tag_read, Unset):
            tag_read = []
            for componentsschemasgpoled_action_v_1_item_data in self.tag_read:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                tag_read.append(componentsschemasgpoled_action_v_1_item)



        radio_start: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.radio_start, Unset):
            radio_start = []
            for componentsschemasgpoled_action_v_1_item_data in self.radio_start:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                radio_start.append(componentsschemasgpoled_action_v_1_item)



        radio_stop: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.radio_stop, Unset):
            radio_stop = []
            for componentsschemasgpoled_action_v_1_item_data in self.radio_stop:
                componentsschemasgpoled_action_v_1_item: dict[str, Any]
                if isinstance(componentsschemasgpoled_action_v_1_item_data, GPOAction):
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()
                else:
                    componentsschemasgpoled_action_v_1_item = componentsschemasgpoled_action_v_1_item_data.to_dict()

                radio_stop.append(componentsschemasgpoled_action_v_1_item)



        gpi_debounce: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.gpi_debounce, Unset):
            gpi_debounce = self.gpi_debounce.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if gpo_defaults is not UNSET:
            field_dict["GPODefaults"] = gpo_defaults
        if led_defaults is not UNSET:
            field_dict["LEDDefaults"] = led_defaults
        if gpi_1_h is not UNSET:
            field_dict["GPI_1_H"] = gpi_1_h
        if gpi_1_l is not UNSET:
            field_dict["GPI_1_L"] = gpi_1_l
        if gpi_2_h is not UNSET:
            field_dict["GPI_2_H"] = gpi_2_h
        if gpi_2_l is not UNSET:
            field_dict["GPI_2_L"] = gpi_2_l
        if cloud_disconnect is not UNSET:
            field_dict["CLOUD_DISCONNECT"] = cloud_disconnect
        if cloud_connect is not UNSET:
            field_dict["CLOUD_CONNECT"] = cloud_connect
        if tag_read is not UNSET:
            field_dict["TAG_READ"] = tag_read
        if radio_start is not UNSET:
            field_dict["RADIO_START"] = radio_start
        if radio_stop is not UNSET:
            field_dict["RADIO_STOP"] = radio_stop
        if gpi_debounce is not UNSET:
            field_dict["GPIDebounce"] = gpi_debounce

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gpioled_configuration_gpo_defaults import GPIOLEDConfigurationGPODefaults
        from ..models.gpioled_configuration_led_defaults import GPIOLEDConfigurationLEDDefaults
        from ..models.led_action import LEDAction
        from ..models.gpo_action import GPOAction
        from ..models.gpioled_configuration_gpi_debounce import GPIOLEDConfigurationGPIDebounce
        d = dict(src_dict)
        _gpo_defaults = d.pop("GPODefaults", UNSET)
        gpo_defaults: Union[Unset, GPIOLEDConfigurationGPODefaults]
        if isinstance(_gpo_defaults,  Unset):
            gpo_defaults = UNSET
        else:
            gpo_defaults = GPIOLEDConfigurationGPODefaults.from_dict(_gpo_defaults)




        _led_defaults = d.pop("LEDDefaults", UNSET)
        led_defaults: Union[Unset, GPIOLEDConfigurationLEDDefaults]
        if isinstance(_led_defaults,  Unset):
            led_defaults = UNSET
        else:
            led_defaults = GPIOLEDConfigurationLEDDefaults.from_dict(_led_defaults)




        gpi_1_h = []
        _gpi_1_h = d.pop("GPI_1_H", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_gpi_1_h or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            gpi_1_h.append(componentsschemasgpoled_action_v_1_item)


        gpi_1_l = []
        _gpi_1_l = d.pop("GPI_1_L", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_gpi_1_l or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            gpi_1_l.append(componentsschemasgpoled_action_v_1_item)


        gpi_2_h = []
        _gpi_2_h = d.pop("GPI_2_H", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_gpi_2_h or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            gpi_2_h.append(componentsschemasgpoled_action_v_1_item)


        gpi_2_l = []
        _gpi_2_l = d.pop("GPI_2_L", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_gpi_2_l or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            gpi_2_l.append(componentsschemasgpoled_action_v_1_item)


        cloud_disconnect = []
        _cloud_disconnect = d.pop("CLOUD_DISCONNECT", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_cloud_disconnect or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            cloud_disconnect.append(componentsschemasgpoled_action_v_1_item)


        cloud_connect = []
        _cloud_connect = d.pop("CLOUD_CONNECT", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_cloud_connect or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            cloud_connect.append(componentsschemasgpoled_action_v_1_item)


        tag_read = []
        _tag_read = d.pop("TAG_READ", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_tag_read or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            tag_read.append(componentsschemasgpoled_action_v_1_item)


        radio_start = []
        _radio_start = d.pop("RADIO_START", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_radio_start or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            radio_start.append(componentsschemasgpoled_action_v_1_item)


        radio_stop = []
        _radio_stop = d.pop("RADIO_STOP", UNSET)
        for componentsschemasgpoled_action_v_1_item_data in (_radio_stop or []):
            def _parse_componentsschemasgpoled_action_v_1_item(data: object) -> Union['GPOAction', 'LEDAction']:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemasgpoled_action_v_1_item_type_0 = GPOAction.from_dict(data)



                    return componentsschemasgpoled_action_v_1_item_type_0
                except: # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemasgpoled_action_v_1_item_type_1 = LEDAction.from_dict(data)



                return componentsschemasgpoled_action_v_1_item_type_1

            componentsschemasgpoled_action_v_1_item = _parse_componentsschemasgpoled_action_v_1_item(componentsschemasgpoled_action_v_1_item_data)

            radio_stop.append(componentsschemasgpoled_action_v_1_item)


        _gpi_debounce = d.pop("GPIDebounce", UNSET)
        gpi_debounce: Union[Unset, GPIOLEDConfigurationGPIDebounce]
        if isinstance(_gpi_debounce,  Unset):
            gpi_debounce = UNSET
        else:
            gpi_debounce = GPIOLEDConfigurationGPIDebounce.from_dict(_gpi_debounce)




        gpioled_configuration = cls(
            gpo_defaults=gpo_defaults,
            led_defaults=led_defaults,
            gpi_1_h=gpi_1_h,
            gpi_1_l=gpi_1_l,
            gpi_2_h=gpi_2_h,
            gpi_2_l=gpi_2_l,
            cloud_disconnect=cloud_disconnect,
            cloud_connect=cloud_connect,
            tag_read=tag_read,
            radio_start=radio_start,
            radio_stop=radio_stop,
            gpi_debounce=gpi_debounce,
        )


        gpioled_configuration.additional_properties = d
        return gpioled_configuration

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
