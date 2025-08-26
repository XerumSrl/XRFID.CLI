from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_reader_capabilites_capabilities_app_led_colors_item import check_get_reader_capabilites_capabilities_app_led_colors_item
from ..models.get_reader_capabilites_capabilities_app_led_colors_item import GetReaderCapabilitesCapabilitiesAppLedColorsItem
from ..models.get_reader_capabilites_capabilities_da_app_package_format_item import check_get_reader_capabilites_capabilities_da_app_package_format_item
from ..models.get_reader_capabilites_capabilities_da_app_package_format_item import GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem
from ..models.get_reader_capabilites_capabilities_da_language_bindings_item import check_get_reader_capabilites_capabilities_da_language_bindings_item
from ..models.get_reader_capabilites_capabilities_da_language_bindings_item import GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem
from ..models.get_reader_capabilites_capabilities_external_serial_port_item import check_get_reader_capabilites_capabilities_external_serial_port_item
from ..models.get_reader_capabilites_capabilities_external_serial_port_item import GetReaderCapabilitesCapabilitiesExternalSerialPortItem
from ..models.get_reader_capabilites_capabilities_keypad_support_item import check_get_reader_capabilites_capabilities_keypad_support_item
from ..models.get_reader_capabilites_capabilities_keypad_support_item import GetReaderCapabilitesCapabilitiesKeypadSupportItem
from ..models.get_reader_capabilites_capabilities_message_formats_supported_item import check_get_reader_capabilites_capabilities_message_formats_supported_item
from ..models.get_reader_capabilites_capabilities_message_formats_supported_item import GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem
from ..models.get_reader_capabilites_capabilities_supported_display_type_item import check_get_reader_capabilites_capabilities_supported_display_type_item
from ..models.get_reader_capabilites_capabilities_supported_display_type_item import GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem
from ..models.get_reader_capabilites_capabilities_supported_power_source_item import check_get_reader_capabilites_capabilities_supported_power_source_item
from ..models.get_reader_capabilites_capabilities_supported_power_source_item import GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem
from ..models.get_reader_capabilites_capabilities_supported_tag_data_format_item import check_get_reader_capabilites_capabilities_supported_tag_data_format_item
from ..models.get_reader_capabilites_capabilities_supported_tag_data_format_item import GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem
from ..models.get_reader_capabilites_capabilities_triggers_item import check_get_reader_capabilites_capabilities_triggers_item
from ..models.get_reader_capabilites_capabilities_triggers_item import GetReaderCapabilitesCapabilitiesTriggersItem
from typing import cast

if TYPE_CHECKING:
  from ..models.get_reader_capabilites_capabilities_api_supported import GetReaderCapabilitesCapabilitiesApiSupported
  from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem
  from ..models.get_reader_capabilites_capabilities_network_interfaces_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItem
  from ..models.get_reader_capabilites_capabilities_antennas_item import GetReaderCapabilitesCapabilitiesAntennasItem





T = TypeVar("T", bound="GetReaderCapabilitesCapabilities")



@_attrs_define
class GetReaderCapabilitesCapabilities:
    """ 
        Attributes:
            antennas (list['GetReaderCapabilitesCapabilitiesAntennasItem']):
            api_supported (GetReaderCapabilitesCapabilitiesApiSupported):
            app_led_colors (list[GetReaderCapabilitesCapabilitiesAppLedColorsItem]): Possible App LED Colors
            async_management_events_supported (bool): Denotes if the reader supports asynchronous management events
            beepers_supported (bool): Denotes if the reader supports Beepers
            clock_support (bool): Denotes if the reader supports Clock
            da_app_package_format (list[GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem]): DA Application Formats
                supported by the reader
            da_apps_supported (bool): Denotes if the reader supports DA Applications
            da_language_bindings (list[GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem]): List of DA Application
                languages supported
            directionality_supported (bool): Denotes if the reader supports Directionality
            endpoint_types_supported (list['GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem']): Types of
                endpoints supported by the reader
            external_serial_port (list[GetReaderCapabilitesCapabilitiesExternalSerialPortItem]): Type of serial port
                interfaces supported by the reader
            keypad_support (list[GetReaderCapabilitesCapabilitiesKeypadSupportItem]): Types of keypads supported by the
                reader
            llrp_supported (bool): Denotes if the reader supports LLRP
            max_app_le_ds (int): Maximum number of app LEDs supported by the reader
            max_data_endpoints (int): Maximum Data endpoints supported by the reader
            max_num_operations_in_access_sequence (int): Maximum number of Access Operations supported
            max_num_pre_filters (int): Maximum number of prefilters supported
            message_formats_supported (list[GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem]): Message formats
                supported by the reader
            network_interfaces (list['GetReaderCapabilitesCapabilitiesNetworkInterfacesItem']):
            num_gp_is (int): Number of GPIs supported
            num_gp_os (int): Number of GPOs supported
            rest_api_supported (bool): Denotes if REST API is supported
            rssi_filter_supported (bool): Denotes if RSSI Filter is supported
            supported_display_type (list[GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem]): Types of Display
                supported
            supported_power_source (list[GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem]): Types of power source
                supported
            supported_tag_data_format (list[GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem]): Tag data formats
                supported
            tag_locationing_supported (bool): Denotes if reader supports tag locationing
            triggers (list[GetReaderCapabilitesCapabilitiesTriggersItem]): Types of triggers supported
     """

    antennas: list['GetReaderCapabilitesCapabilitiesAntennasItem']
    api_supported: 'GetReaderCapabilitesCapabilitiesApiSupported'
    app_led_colors: list[GetReaderCapabilitesCapabilitiesAppLedColorsItem]
    async_management_events_supported: bool
    beepers_supported: bool
    clock_support: bool
    da_app_package_format: list[GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem]
    da_apps_supported: bool
    da_language_bindings: list[GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem]
    directionality_supported: bool
    endpoint_types_supported: list['GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem']
    external_serial_port: list[GetReaderCapabilitesCapabilitiesExternalSerialPortItem]
    keypad_support: list[GetReaderCapabilitesCapabilitiesKeypadSupportItem]
    llrp_supported: bool
    max_app_le_ds: int
    max_data_endpoints: int
    max_num_operations_in_access_sequence: int
    max_num_pre_filters: int
    message_formats_supported: list[GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem]
    network_interfaces: list['GetReaderCapabilitesCapabilitiesNetworkInterfacesItem']
    num_gp_is: int
    num_gp_os: int
    rest_api_supported: bool
    rssi_filter_supported: bool
    supported_display_type: list[GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem]
    supported_power_source: list[GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem]
    supported_tag_data_format: list[GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem]
    tag_locationing_supported: bool
    triggers: list[GetReaderCapabilitesCapabilitiesTriggersItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.get_reader_capabilites_capabilities_api_supported import GetReaderCapabilitesCapabilitiesApiSupported
        from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem
        from ..models.get_reader_capabilites_capabilities_network_interfaces_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItem
        from ..models.get_reader_capabilites_capabilities_antennas_item import GetReaderCapabilitesCapabilitiesAntennasItem
        antennas = []
        for antennas_item_data in self.antennas:
            antennas_item = antennas_item_data.to_dict()
            antennas.append(antennas_item)



        api_supported = self.api_supported.to_dict()

        app_led_colors = []
        for app_led_colors_item_data in self.app_led_colors:
            app_led_colors_item: str = app_led_colors_item_data
            app_led_colors.append(app_led_colors_item)



        async_management_events_supported = self.async_management_events_supported

        beepers_supported = self.beepers_supported

        clock_support = self.clock_support

        da_app_package_format = []
        for da_app_package_format_item_data in self.da_app_package_format:
            da_app_package_format_item: str = da_app_package_format_item_data
            da_app_package_format.append(da_app_package_format_item)



        da_apps_supported = self.da_apps_supported

        da_language_bindings = []
        for da_language_bindings_item_data in self.da_language_bindings:
            da_language_bindings_item: str = da_language_bindings_item_data
            da_language_bindings.append(da_language_bindings_item)



        directionality_supported = self.directionality_supported

        endpoint_types_supported = []
        for endpoint_types_supported_item_data in self.endpoint_types_supported:
            endpoint_types_supported_item = endpoint_types_supported_item_data.to_dict()
            endpoint_types_supported.append(endpoint_types_supported_item)



        external_serial_port = []
        for external_serial_port_item_data in self.external_serial_port:
            external_serial_port_item: str = external_serial_port_item_data
            external_serial_port.append(external_serial_port_item)



        keypad_support = []
        for keypad_support_item_data in self.keypad_support:
            keypad_support_item: str = keypad_support_item_data
            keypad_support.append(keypad_support_item)



        llrp_supported = self.llrp_supported

        max_app_le_ds = self.max_app_le_ds

        max_data_endpoints = self.max_data_endpoints

        max_num_operations_in_access_sequence = self.max_num_operations_in_access_sequence

        max_num_pre_filters = self.max_num_pre_filters

        message_formats_supported = []
        for message_formats_supported_item_data in self.message_formats_supported:
            message_formats_supported_item: str = message_formats_supported_item_data
            message_formats_supported.append(message_formats_supported_item)



        network_interfaces = []
        for network_interfaces_item_data in self.network_interfaces:
            network_interfaces_item = network_interfaces_item_data.to_dict()
            network_interfaces.append(network_interfaces_item)



        num_gp_is = self.num_gp_is

        num_gp_os = self.num_gp_os

        rest_api_supported = self.rest_api_supported

        rssi_filter_supported = self.rssi_filter_supported

        supported_display_type = []
        for supported_display_type_item_data in self.supported_display_type:
            supported_display_type_item: str = supported_display_type_item_data
            supported_display_type.append(supported_display_type_item)



        supported_power_source = []
        for supported_power_source_item_data in self.supported_power_source:
            supported_power_source_item: str = supported_power_source_item_data
            supported_power_source.append(supported_power_source_item)



        supported_tag_data_format = []
        for supported_tag_data_format_item_data in self.supported_tag_data_format:
            supported_tag_data_format_item: str = supported_tag_data_format_item_data
            supported_tag_data_format.append(supported_tag_data_format_item)



        tag_locationing_supported = self.tag_locationing_supported

        triggers = []
        for triggers_item_data in self.triggers:
            triggers_item: str = triggers_item_data
            triggers.append(triggers_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "antennas": antennas,
            "apiSupported": api_supported,
            "appLedColors": app_led_colors,
            "asyncManagementEventsSupported": async_management_events_supported,
            "beepersSupported": beepers_supported,
            "clockSupport": clock_support,
            "daAppPackageFormat": da_app_package_format,
            "daAppsSupported": da_apps_supported,
            "daLanguageBindings": da_language_bindings,
            "directionalitySupported": directionality_supported,
            "endpointTypesSupported": endpoint_types_supported,
            "externalSerialPort": external_serial_port,
            "keypadSupport": keypad_support,
            "llrpSupported": llrp_supported,
            "maxAppLEDs": max_app_le_ds,
            "maxDataEndpoints": max_data_endpoints,
            "maxNumOperationsInAccessSequence": max_num_operations_in_access_sequence,
            "maxNumPreFilters": max_num_pre_filters,
            "messageFormatsSupported": message_formats_supported,
            "networkInterfaces": network_interfaces,
            "numGPIs": num_gp_is,
            "numGPOs": num_gp_os,
            "restAPISupported": rest_api_supported,
            "rssiFilterSupported": rssi_filter_supported,
            "supportedDisplayType": supported_display_type,
            "supportedPowerSource": supported_power_source,
            "supportedTagDataFormat": supported_tag_data_format,
            "tagLocationingSupported": tag_locationing_supported,
            "triggers": triggers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_reader_capabilites_capabilities_api_supported import GetReaderCapabilitesCapabilitiesApiSupported
        from ..models.get_reader_capabilites_capabilities_endpoint_types_supported_item import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem
        from ..models.get_reader_capabilites_capabilities_network_interfaces_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItem
        from ..models.get_reader_capabilites_capabilities_antennas_item import GetReaderCapabilitesCapabilitiesAntennasItem
        d = dict(src_dict)
        antennas = []
        _antennas = d.pop("antennas")
        for antennas_item_data in (_antennas):
            antennas_item = GetReaderCapabilitesCapabilitiesAntennasItem.from_dict(antennas_item_data)



            antennas.append(antennas_item)


        api_supported = GetReaderCapabilitesCapabilitiesApiSupported.from_dict(d.pop("apiSupported"))




        app_led_colors = []
        _app_led_colors = d.pop("appLedColors")
        for app_led_colors_item_data in (_app_led_colors):
            app_led_colors_item = check_get_reader_capabilites_capabilities_app_led_colors_item(app_led_colors_item_data)



            app_led_colors.append(app_led_colors_item)


        async_management_events_supported = d.pop("asyncManagementEventsSupported")

        beepers_supported = d.pop("beepersSupported")

        clock_support = d.pop("clockSupport")

        da_app_package_format = []
        _da_app_package_format = d.pop("daAppPackageFormat")
        for da_app_package_format_item_data in (_da_app_package_format):
            da_app_package_format_item = check_get_reader_capabilites_capabilities_da_app_package_format_item(da_app_package_format_item_data)



            da_app_package_format.append(da_app_package_format_item)


        da_apps_supported = d.pop("daAppsSupported")

        da_language_bindings = []
        _da_language_bindings = d.pop("daLanguageBindings")
        for da_language_bindings_item_data in (_da_language_bindings):
            da_language_bindings_item = check_get_reader_capabilites_capabilities_da_language_bindings_item(da_language_bindings_item_data)



            da_language_bindings.append(da_language_bindings_item)


        directionality_supported = d.pop("directionalitySupported")

        endpoint_types_supported = []
        _endpoint_types_supported = d.pop("endpointTypesSupported")
        for endpoint_types_supported_item_data in (_endpoint_types_supported):
            endpoint_types_supported_item = GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem.from_dict(endpoint_types_supported_item_data)



            endpoint_types_supported.append(endpoint_types_supported_item)


        external_serial_port = []
        _external_serial_port = d.pop("externalSerialPort")
        for external_serial_port_item_data in (_external_serial_port):
            external_serial_port_item = check_get_reader_capabilites_capabilities_external_serial_port_item(external_serial_port_item_data)



            external_serial_port.append(external_serial_port_item)


        keypad_support = []
        _keypad_support = d.pop("keypadSupport")
        for keypad_support_item_data in (_keypad_support):
            keypad_support_item = check_get_reader_capabilites_capabilities_keypad_support_item(keypad_support_item_data)



            keypad_support.append(keypad_support_item)


        llrp_supported = d.pop("llrpSupported")

        max_app_le_ds = d.pop("maxAppLEDs")

        max_data_endpoints = d.pop("maxDataEndpoints")

        max_num_operations_in_access_sequence = d.pop("maxNumOperationsInAccessSequence")

        max_num_pre_filters = d.pop("maxNumPreFilters")

        message_formats_supported = []
        _message_formats_supported = d.pop("messageFormatsSupported")
        for message_formats_supported_item_data in (_message_formats_supported):
            message_formats_supported_item = check_get_reader_capabilites_capabilities_message_formats_supported_item(message_formats_supported_item_data)



            message_formats_supported.append(message_formats_supported_item)


        network_interfaces = []
        _network_interfaces = d.pop("networkInterfaces")
        for network_interfaces_item_data in (_network_interfaces):
            network_interfaces_item = GetReaderCapabilitesCapabilitiesNetworkInterfacesItem.from_dict(network_interfaces_item_data)



            network_interfaces.append(network_interfaces_item)


        num_gp_is = d.pop("numGPIs")

        num_gp_os = d.pop("numGPOs")

        rest_api_supported = d.pop("restAPISupported")

        rssi_filter_supported = d.pop("rssiFilterSupported")

        supported_display_type = []
        _supported_display_type = d.pop("supportedDisplayType")
        for supported_display_type_item_data in (_supported_display_type):
            supported_display_type_item = check_get_reader_capabilites_capabilities_supported_display_type_item(supported_display_type_item_data)



            supported_display_type.append(supported_display_type_item)


        supported_power_source = []
        _supported_power_source = d.pop("supportedPowerSource")
        for supported_power_source_item_data in (_supported_power_source):
            supported_power_source_item = check_get_reader_capabilites_capabilities_supported_power_source_item(supported_power_source_item_data)



            supported_power_source.append(supported_power_source_item)


        supported_tag_data_format = []
        _supported_tag_data_format = d.pop("supportedTagDataFormat")
        for supported_tag_data_format_item_data in (_supported_tag_data_format):
            supported_tag_data_format_item = check_get_reader_capabilites_capabilities_supported_tag_data_format_item(supported_tag_data_format_item_data)



            supported_tag_data_format.append(supported_tag_data_format_item)


        tag_locationing_supported = d.pop("tagLocationingSupported")

        triggers = []
        _triggers = d.pop("triggers")
        for triggers_item_data in (_triggers):
            triggers_item = check_get_reader_capabilites_capabilities_triggers_item(triggers_item_data)



            triggers.append(triggers_item)


        get_reader_capabilites_capabilities = cls(
            antennas=antennas,
            api_supported=api_supported,
            app_led_colors=app_led_colors,
            async_management_events_supported=async_management_events_supported,
            beepers_supported=beepers_supported,
            clock_support=clock_support,
            da_app_package_format=da_app_package_format,
            da_apps_supported=da_apps_supported,
            da_language_bindings=da_language_bindings,
            directionality_supported=directionality_supported,
            endpoint_types_supported=endpoint_types_supported,
            external_serial_port=external_serial_port,
            keypad_support=keypad_support,
            llrp_supported=llrp_supported,
            max_app_le_ds=max_app_le_ds,
            max_data_endpoints=max_data_endpoints,
            max_num_operations_in_access_sequence=max_num_operations_in_access_sequence,
            max_num_pre_filters=max_num_pre_filters,
            message_formats_supported=message_formats_supported,
            network_interfaces=network_interfaces,
            num_gp_is=num_gp_is,
            num_gp_os=num_gp_os,
            rest_api_supported=rest_api_supported,
            rssi_filter_supported=rssi_filter_supported,
            supported_display_type=supported_display_type,
            supported_power_source=supported_power_source,
            supported_tag_data_format=supported_tag_data_format,
            tag_locationing_supported=tag_locationing_supported,
            triggers=triggers,
        )


        get_reader_capabilites_capabilities.additional_properties = d
        return get_reader_capabilites_capabilities

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
