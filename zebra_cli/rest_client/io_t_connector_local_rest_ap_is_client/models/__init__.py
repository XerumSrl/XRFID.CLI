""" Contains all the data models used in inputs/outputs """

from .access import Access
from .access_config import AccessConfig
from .access_type import AccessType
from .action_blink_configuration import ActionBlinkConfiguration
from .action_conditions_v1_type_1 import ActionConditionsV1Type1
from .action_conditions_v1_type_1_operator import ActionConditionsV1Type1Operator
from .all_ import All
from .antenna_stop_condition import AntennaStopCondition
from .antenna_stop_condition_type import AntennaStopConditionType
from .aws import AWS
from .aws_additional import AWSAdditional
from .aws_additional_qos import AWSAdditionalQos
from .aws_endpoint import AWSEndpoint
from .aws_security import AWSSecurity
from .azure import AZURE
from .azure_additional import AZUREAdditional
from .azure_additional_qos import AZUREAdditionalQos
from .azure_basic_authentication import AZUREBasicAuthentication
from .azure_endpoint import AZUREEndpoint
from .azure_security import AZURESecurity
from .basic_authentication_for_external_server_connections import BasicAuthenticationForExternalServerConnections
from .conditions_array_v1_item import ConditionsArrayV1Item
from .cpu_stats import CpuStats
from .del_certificate_body import DelCertificateBody
from .del_certificate_body_type import DelCertificateBodyType
from .del_logs_syslog_log_type import DelLogsSyslogLogType
from .delay_between_antenna_cycles import DelayBetweenAntennaCycles
from .delay_between_antenna_cycles_type import DelayBetweenAntennaCyclesType
from .directionality_settings import DirectionalitySettings
from .directionality_settings_aar import DirectionalitySettingsAar
from .directionality_settings_advanced_config import DirectionalitySettingsAdvancedConfig
from .directionality_settings_advanced_config_debug_level import DirectionalitySettingsAdvancedConfigDebugLevel
from .directionality_settings_advanced_config_report_direction_item import DirectionalitySettingsAdvancedConfigReportDirectionItem
from .directionality_settings_advanced_config_user_defined_type_1 import DirectionalitySettingsAdvancedConfigUserDefinedType1
from .directionality_settings_basic_config import DirectionalitySettingsBasicConfig
from .directionality_settings_basic_config_beams import DirectionalitySettingsBasicConfigBeams
from .directionality_settings_basic_config_beams_beams_item import DirectionalitySettingsBasicConfigBeamsBeamsItem
from .directionality_settings_basic_config_beams_beams_item_polarization import DirectionalitySettingsBasicConfigBeamsBeamsItemPolarization
from .directionality_settings_basic_config_density import DirectionalitySettingsBasicConfigDensity
from .directionality_settings_basic_config_density_density import DirectionalitySettingsBasicConfigDensityDensity
from .directionality_settings_basic_config_density_density_polarization import DirectionalitySettingsBasicConfigDensityDensityPolarization
from .directionality_settings_basic_config_density_density_type import DirectionalitySettingsBasicConfigDensityDensityType
from .directionality_settings_basic_config_zone_plan import DirectionalitySettingsBasicConfigZonePlan
from .each_read_point import EachReadPoint
from .endpoint_info_object import EndpointInfoObject
from .endpoint_info_object_protocol import EndpointInfoObjectProtocol
from .error import Error
from .event import Event
from .event_connections_item import EventConnectionsItem
from .event_connections_item_additional_options import EventConnectionsItemAdditionalOptions
from .event_connections_item_type import EventConnectionsItemType
from .get_appled_response_200 import GetAppledResponse200
from .get_cable_loss_compensation import GetCableLossCompensation
from .get_cable_loss_compensation_read_point import GetCableLossCompensationReadPoint
from .get_certificates_response_200 import GetCertificatesResponse200
from .get_certificates_response_200_type import GetCertificatesResponse200Type
from .get_gpi_status_response_200 import GetGpiStatusResponse200
from .get_gpi_status_response_2001 import GetGpiStatusResponse2001
from .get_gpi_status_response_2002 import GetGpiStatusResponse2002
from .get_gpi_status_response_2003 import GetGpiStatusResponse2003
from .get_gpo_status_response_200 import GetGpoStatusResponse200
from .get_gpo_status_response_2001 import GetGpoStatusResponse2001
from .get_gpo_status_response_2002 import GetGpoStatusResponse2002
from .get_gpo_status_response_2003 import GetGpoStatusResponse2003
from .get_gpo_status_response_2004 import GetGpoStatusResponse2004
from .get_logs_syslog_log_type import GetLogsSyslogLogType
from .get_mode_body import GetModeBody
from .get_name_and_description import GetNameAndDescription
from .get_reader_capabilites import GetReaderCapabilites
from .get_reader_capabilites_capabilities import GetReaderCapabilitesCapabilities
from .get_reader_capabilites_capabilities_antennas_item import GetReaderCapabilitesCapabilitiesAntennasItem
from .get_reader_capabilites_capabilities_antennas_item_type import GetReaderCapabilitesCapabilitiesAntennasItemType
from .get_reader_capabilites_capabilities_api_supported import GetReaderCapabilitesCapabilitiesApiSupported
from .get_reader_capabilites_capabilities_api_supported_versions import GetReaderCapabilitesCapabilitiesApiSupportedVersions
from .get_reader_capabilites_capabilities_api_supported_versions_version import GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion
from .get_reader_capabilites_capabilities_app_led_colors_item import GetReaderCapabilitesCapabilitiesAppLedColorsItem
from .get_reader_capabilites_capabilities_da_app_package_format_item import GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem
from .get_reader_capabilites_capabilities_da_language_bindings_item import GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem
from .get_reader_capabilites_capabilities_endpoint_types_supported_item import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem
from .get_reader_capabilites_capabilities_endpoint_types_supported_item_authentication_types_supported_item import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem
from .get_reader_capabilites_capabilities_endpoint_types_supported_item_type import GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType
from .get_reader_capabilites_capabilities_external_serial_port_item import GetReaderCapabilitesCapabilitiesExternalSerialPortItem
from .get_reader_capabilites_capabilities_keypad_support_item import GetReaderCapabilitesCapabilitiesKeypadSupportItem
from .get_reader_capabilites_capabilities_message_formats_supported_item import GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem
from .get_reader_capabilites_capabilities_network_interfaces_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItem
from .get_reader_capabilites_capabilities_network_interfaces_item_ip_assignment_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem
from .get_reader_capabilites_capabilities_network_interfaces_item_ip_stack_item import GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem
from .get_reader_capabilites_capabilities_network_interfaces_item_type import GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType
from .get_reader_capabilites_capabilities_supported_display_type_item import GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem
from .get_reader_capabilites_capabilities_supported_power_source_item import GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem
from .get_reader_capabilites_capabilities_supported_tag_data_format_item import GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem
from .get_reader_capabilites_capabilities_triggers_item import GetReaderCapabilitesCapabilitiesTriggersItem
from .get_supported_region_list import GetSupportedRegionList
from .get_time_zone import GetTimeZone
from .get_time_zone_time_zone import GetTimeZoneTimeZone
from .get_userapps_response_200_item import GetUserappsResponse200Item
from .gpi import Gpi
from .gpi_signal import GpiSignal
from .gpioled_configuration import GPIOLEDConfiguration
from .gpioled_configuration_gpi_debounce import GPIOLEDConfigurationGPIDebounce
from .gpioled_configuration_gpo_defaults import GPIOLEDConfigurationGPODefaults
from .gpioled_configuration_gpo_defaults_1 import GPIOLEDConfigurationGPODefaults1
from .gpioled_configuration_gpo_defaults_2 import GPIOLEDConfigurationGPODefaults2
from .gpioled_configuration_gpo_defaults_3 import GPIOLEDConfigurationGPODefaults3
from .gpioled_configuration_gpo_defaults_4 import GPIOLEDConfigurationGPODefaults4
from .gpioled_configuration_led_defaults import GPIOLEDConfigurationLEDDefaults
from .gpioled_configuration_led_defaults_1 import GPIOLEDConfigurationLEDDefaults1
from .gpioled_configuration_led_defaults_2 import GPIOLEDConfigurationLEDDefaults2
from .gpioled_configuration_led_defaults_3 import GPIOLEDConfigurationLEDDefaults3
from .gpo_action import GPOAction
from .gpo_action_pin import GPOActionPin
from .gpo_action_post_action_state import GPOActionPostActionState
from .gpo_action_state import GPOActionState
from .gpo_action_type import GPOActionType
from .http_post import HTTPPost
from .http_post_basic_authentication import HTTPPostBasicAuthentication
from .http_post_security import HTTPPostSecurity
from .http_post_security_authentication_type import HTTPPostSecurityAuthenticationType
from .http_post_tls_authentication import HTTPPostTLSAuthentication
from .inventory_settings import InventorySettings
from .inventory_settings_interval import InventorySettingsInterval
from .inventory_settings_interval_unit import InventorySettingsIntervalUnit
from .keyboard_emulation import KeyboardEmulation
from .keyboard_emulation_additional_config import KeyboardEmulationAdditionalConfig
from .keyboard_emulation_line_ending import KeyboardEmulationLineEnding
from .kill import Kill
from .kill_config import KillConfig
from .kill_type import KillType
from .led_action import LEDAction
from .led_action_color import LEDActionColor
from .led_action_led import LEDActionLed
from .led_action_post_action_color import LEDActionPostActionColor
from .led_action_type import LEDActionType
from .lock import Lock
from .lock_config import LockConfig
from .lock_config_actions_item import LockConfigActionsItem
from .lock_type import LockType
from .log_level import LogLevel
from .log_level_components_item import LogLevelComponentsItem
from .log_level_components_item_component_name import LogLevelComponentsItemComponentName
from .log_level_components_item_level import LogLevelComponentsItemLevel
from .management_events_configuration import ManagementEventsConfiguration
from .management_events_configuration_errors import ManagementEventsConfigurationErrors
from .management_events_configuration_errors_cpu import ManagementEventsConfigurationErrorsCpu
from .management_events_configuration_errors_flash import ManagementEventsConfigurationErrorsFlash
from .management_events_configuration_errors_ram import ManagementEventsConfigurationErrorsRam
from .management_events_configuration_errors_userapp import ManagementEventsConfigurationErrorsUserapp
from .management_events_configuration_heartbeat import ManagementEventsConfigurationHeartbeat
from .management_events_configuration_heartbeat_fields import ManagementEventsConfigurationHeartbeatFields
from .management_events_configuration_heartbeat_fields_radio_control_item import ManagementEventsConfigurationHeartbeatFieldsRadioControlItem
from .management_events_configuration_heartbeat_fields_reader_gateway_item import ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem
from .management_events_configuration_heartbeat_fields_system_item import ManagementEventsConfigurationHeartbeatFieldsSystemItem
from .management_events_configuration_heartbeat_fields_user_defined import ManagementEventsConfigurationHeartbeatFieldsUserDefined
from .management_events_configuration_heartbeat_fields_userapps_item import ManagementEventsConfigurationHeartbeatFieldsUserappsItem
from .management_events_configuration_warnings import ManagementEventsConfigurationWarnings
from .management_events_configuration_warnings_cpu import ManagementEventsConfigurationWarningsCpu
from .management_events_configuration_warnings_flash import ManagementEventsConfigurationWarningsFlash
from .management_events_configuration_warnings_ntp_type_0 import ManagementEventsConfigurationWarningsNtpType0
from .management_events_configuration_warnings_ram import ManagementEventsConfigurationWarningsRam
from .management_events_configuration_warnings_temperature import ManagementEventsConfigurationWarningsTemperature
from .management_events_configuration_warnings_userapp import ManagementEventsConfigurationWarningsUserapp
from .memory_stats import MemoryStats
from .mqtt import MQTT
from .mqtt_additional_options import MQTTAdditionalOptions
from .mqtt_security import MQTTSecurity
from .mqtt_security_key_algorithm import MQTTSecurityKeyAlgorithm
from .mqtt_security_key_format import MQTTSecurityKeyFormat
from .network_config import NetworkConfig
from .ntpstats import Ntpstats
from .operating_mode import OperatingMode
from .operating_mode_beams_item import OperatingModeBeamsItem
from .operating_mode_beams_item_polarization import OperatingModeBeamsItemPolarization
from .operating_mode_environment import OperatingModeEnvironment
from .operating_mode_type import OperatingModeType
from .os_update import OsUpdate
from .os_update_authentication_type import OsUpdateAuthenticationType
from .os_update_options import OsUpdateOptions
from .os_versions import OsVersions
from .portal_settings import PortalSettings
from .portal_settings_start_trigger import PortalSettingsStartTrigger
from .portal_settings_start_trigger_port import PortalSettingsStartTriggerPort
from .portal_settings_start_trigger_signal import PortalSettingsStartTriggerSignal
from .query import Query
from .query_sel import QuerySel
from .query_session import QuerySession
from .query_target import QueryTarget
from .radio_start_conditions import RadioStartConditions
from .radio_start_conditions_type import RadioStartConditionsType
from .radio_stop_conditions import RadioStopConditions
from .read import Read
from .read_config import ReadConfig
from .read_config_membank import ReadConfigMembank
from .read_type import ReadType
from .reader_flash_memory import ReaderFlashMemory
from .reader_interface_connection_status import ReaderInterfaceConnectionStatus
from .reader_interface_connection_status_data_item import ReaderInterfaceConnectionStatusDataItem
from .reader_interface_connection_status_data_item_connection_status import ReaderInterfaceConnectionStatusDataItemConnectionStatus
from .reader_network import ReaderNetwork
from .reader_stats import ReaderStats
from .reader_stats_antennas import ReaderStatsAntennas
from .reader_stats_antennas_0 import ReaderStatsAntennas0
from .reader_stats_antennas_1 import ReaderStatsAntennas1
from .reader_stats_antennas_10 import ReaderStatsAntennas10
from .reader_stats_antennas_11 import ReaderStatsAntennas11
from .reader_stats_antennas_12 import ReaderStatsAntennas12
from .reader_stats_antennas_13 import ReaderStatsAntennas13
from .reader_stats_antennas_2 import ReaderStatsAntennas2
from .reader_stats_antennas_3 import ReaderStatsAntennas3
from .reader_stats_antennas_4 import ReaderStatsAntennas4
from .reader_stats_antennas_5 import ReaderStatsAntennas5
from .reader_stats_antennas_6 import ReaderStatsAntennas6
from .reader_stats_antennas_7 import ReaderStatsAntennas7
from .reader_stats_antennas_8 import ReaderStatsAntennas8
from .reader_stats_antennas_9 import ReaderStatsAntennas9
from .reader_stats_ntp_type_1 import ReaderStatsNtpType1
from .reader_stats_power_negotiation import ReaderStatsPowerNegotiation
from .reader_stats_power_source import ReaderStatsPowerSource
from .reader_stats_radio_activitiy import ReaderStatsRadioActivitiy
from .reader_stats_radio_connection import ReaderStatsRadioConnection
from .reader_upgrade_status import ReaderUpgradeStatus
from .reader_upgrade_status_status import ReaderUpgradeStatusStatus
from .reader_upgrade_status_update_progress_details import ReaderUpgradeStatusUpdateProgressDetails
from .reader_version import ReaderVersion
from .reader_version_model import ReaderVersionModel
from .reader_version_revert_back_firmware import ReaderVersionRevertBackFirmware
from .region_config import RegionConfig
from .region_config_max_tx_power_supported import RegionConfigMaxTxPowerSupported
from .region_config_min_tx_power_supported import RegionConfigMinTxPowerSupported
from .report_filter import ReportFilter
from .report_filter_type import ReportFilterType
from .rssi_filter import RssiFilter
from .select import Select
from .select_action import SelectAction
from .select_membank import SelectMembank
from .select_target import SelectTarget
from .set_appled_color import SetAppledColor
from .set_autostart_userapp_body import SetAutostartUserappBody
from .set_gpo_body import SetGpoBody
from .set_install_userapp_body import SetInstallUserappBody
from .set_install_userapp_body_authentication_type import SetInstallUserappBodyAuthenticationType
from .set_install_userapp_body_options import SetInstallUserappBodyOptions
from .set_name_and_description import SetNameAndDescription
from .set_ntp_server import SetNTPServer
from .set_refresh_certificate_body import SetRefreshCertificateBody
from .set_refresh_certificate_body_type import SetRefreshCertificateBodyType
from .set_req_to_userapp_body import SetReqToUserappBody
from .set_req_to_userapp_response_200 import SetReqToUserappResponse200
from .set_time_zone import SetTimeZone
from .set_time_zone_time_zone import SetTimeZoneTimeZone
from .set_update_certificate import SetUpdateCertificate
from .set_update_certificate_authentication_type import SetUpdateCertificateAuthenticationType
from .set_update_certificate_headers import SetUpdateCertificateHeaders
from .set_update_certificate_options import SetUpdateCertificateOptions
from .set_update_certificate_type import SetUpdateCertificateType
from .start import Start
from .supported_standard_list import SupportedStandardList
from .supported_standard_list_region import SupportedStandardListRegion
from .supported_standardlist import SupportedStandardlist
from .supported_standardlist_supported_standards_item import SupportedStandardlistSupportedStandardsItem
from .tag_data_events_batching_configuration import TagDataEventsBatchingConfiguration
from .tag_data_events_retention_configuration import TagDataEventsRetentionConfiguration
from .tag_id_filter import TagIdFilter
from .tag_id_filter_match import TagIdFilterMatch
from .tag_id_filter_operation import TagIdFilterOperation
from .tag_meta_data_v1_item import TagMetaDataV1Item
from .tcpip import TCPIP
from .tcpip_security import TCPIPSecurity
from .websocket import Websocket
from .websocket_security import WebsocketSecurity
from .write import Write
from .write_config import WriteConfig
from .write_config_membank import WriteConfigMembank
from .write_type import WriteType

__all__ = (
    "Access",
    "AccessConfig",
    "AccessType",
    "ActionBlinkConfiguration",
    "ActionConditionsV1Type1",
    "ActionConditionsV1Type1Operator",
    "All",
    "AntennaStopCondition",
    "AntennaStopConditionType",
    "AWS",
    "AWSAdditional",
    "AWSAdditionalQos",
    "AWSEndpoint",
    "AWSSecurity",
    "AZURE",
    "AZUREAdditional",
    "AZUREAdditionalQos",
    "AZUREBasicAuthentication",
    "AZUREEndpoint",
    "AZURESecurity",
    "BasicAuthenticationForExternalServerConnections",
    "ConditionsArrayV1Item",
    "CpuStats",
    "DelayBetweenAntennaCycles",
    "DelayBetweenAntennaCyclesType",
    "DelCertificateBody",
    "DelCertificateBodyType",
    "DelLogsSyslogLogType",
    "DirectionalitySettings",
    "DirectionalitySettingsAar",
    "DirectionalitySettingsAdvancedConfig",
    "DirectionalitySettingsAdvancedConfigDebugLevel",
    "DirectionalitySettingsAdvancedConfigReportDirectionItem",
    "DirectionalitySettingsAdvancedConfigUserDefinedType1",
    "DirectionalitySettingsBasicConfig",
    "DirectionalitySettingsBasicConfigBeams",
    "DirectionalitySettingsBasicConfigBeamsBeamsItem",
    "DirectionalitySettingsBasicConfigBeamsBeamsItemPolarization",
    "DirectionalitySettingsBasicConfigDensity",
    "DirectionalitySettingsBasicConfigDensityDensity",
    "DirectionalitySettingsBasicConfigDensityDensityPolarization",
    "DirectionalitySettingsBasicConfigDensityDensityType",
    "DirectionalitySettingsBasicConfigZonePlan",
    "EachReadPoint",
    "EndpointInfoObject",
    "EndpointInfoObjectProtocol",
    "Error",
    "Event",
    "EventConnectionsItem",
    "EventConnectionsItemAdditionalOptions",
    "EventConnectionsItemType",
    "GetAppledResponse200",
    "GetCableLossCompensation",
    "GetCableLossCompensationReadPoint",
    "GetCertificatesResponse200",
    "GetCertificatesResponse200Type",
    "GetGpiStatusResponse200",
    "GetGpiStatusResponse2001",
    "GetGpiStatusResponse2002",
    "GetGpiStatusResponse2003",
    "GetGpoStatusResponse200",
    "GetGpoStatusResponse2001",
    "GetGpoStatusResponse2002",
    "GetGpoStatusResponse2003",
    "GetGpoStatusResponse2004",
    "GetLogsSyslogLogType",
    "GetModeBody",
    "GetNameAndDescription",
    "GetReaderCapabilites",
    "GetReaderCapabilitesCapabilities",
    "GetReaderCapabilitesCapabilitiesAntennasItem",
    "GetReaderCapabilitesCapabilitiesAntennasItemType",
    "GetReaderCapabilitesCapabilitiesApiSupported",
    "GetReaderCapabilitesCapabilitiesApiSupportedVersions",
    "GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion",
    "GetReaderCapabilitesCapabilitiesAppLedColorsItem",
    "GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem",
    "GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem",
    "GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItem",
    "GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem",
    "GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType",
    "GetReaderCapabilitesCapabilitiesExternalSerialPortItem",
    "GetReaderCapabilitesCapabilitiesKeypadSupportItem",
    "GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem",
    "GetReaderCapabilitesCapabilitiesNetworkInterfacesItem",
    "GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem",
    "GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem",
    "GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType",
    "GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem",
    "GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem",
    "GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem",
    "GetReaderCapabilitesCapabilitiesTriggersItem",
    "GetSupportedRegionList",
    "GetTimeZone",
    "GetTimeZoneTimeZone",
    "GetUserappsResponse200Item",
    "Gpi",
    "GPIOLEDConfiguration",
    "GPIOLEDConfigurationGPIDebounce",
    "GPIOLEDConfigurationGPODefaults",
    "GPIOLEDConfigurationGPODefaults1",
    "GPIOLEDConfigurationGPODefaults2",
    "GPIOLEDConfigurationGPODefaults3",
    "GPIOLEDConfigurationGPODefaults4",
    "GPIOLEDConfigurationLEDDefaults",
    "GPIOLEDConfigurationLEDDefaults1",
    "GPIOLEDConfigurationLEDDefaults2",
    "GPIOLEDConfigurationLEDDefaults3",
    "GpiSignal",
    "GPOAction",
    "GPOActionPin",
    "GPOActionPostActionState",
    "GPOActionState",
    "GPOActionType",
    "HTTPPost",
    "HTTPPostBasicAuthentication",
    "HTTPPostSecurity",
    "HTTPPostSecurityAuthenticationType",
    "HTTPPostTLSAuthentication",
    "InventorySettings",
    "InventorySettingsInterval",
    "InventorySettingsIntervalUnit",
    "KeyboardEmulation",
    "KeyboardEmulationAdditionalConfig",
    "KeyboardEmulationLineEnding",
    "Kill",
    "KillConfig",
    "KillType",
    "LEDAction",
    "LEDActionColor",
    "LEDActionLed",
    "LEDActionPostActionColor",
    "LEDActionType",
    "Lock",
    "LockConfig",
    "LockConfigActionsItem",
    "LockType",
    "LogLevel",
    "LogLevelComponentsItem",
    "LogLevelComponentsItemComponentName",
    "LogLevelComponentsItemLevel",
    "ManagementEventsConfiguration",
    "ManagementEventsConfigurationErrors",
    "ManagementEventsConfigurationErrorsCpu",
    "ManagementEventsConfigurationErrorsFlash",
    "ManagementEventsConfigurationErrorsRam",
    "ManagementEventsConfigurationErrorsUserapp",
    "ManagementEventsConfigurationHeartbeat",
    "ManagementEventsConfigurationHeartbeatFields",
    "ManagementEventsConfigurationHeartbeatFieldsRadioControlItem",
    "ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem",
    "ManagementEventsConfigurationHeartbeatFieldsSystemItem",
    "ManagementEventsConfigurationHeartbeatFieldsUserappsItem",
    "ManagementEventsConfigurationHeartbeatFieldsUserDefined",
    "ManagementEventsConfigurationWarnings",
    "ManagementEventsConfigurationWarningsCpu",
    "ManagementEventsConfigurationWarningsFlash",
    "ManagementEventsConfigurationWarningsNtpType0",
    "ManagementEventsConfigurationWarningsRam",
    "ManagementEventsConfigurationWarningsTemperature",
    "ManagementEventsConfigurationWarningsUserapp",
    "MemoryStats",
    "MQTT",
    "MQTTAdditionalOptions",
    "MQTTSecurity",
    "MQTTSecurityKeyAlgorithm",
    "MQTTSecurityKeyFormat",
    "NetworkConfig",
    "Ntpstats",
    "OperatingMode",
    "OperatingModeBeamsItem",
    "OperatingModeBeamsItemPolarization",
    "OperatingModeEnvironment",
    "OperatingModeType",
    "OsUpdate",
    "OsUpdateAuthenticationType",
    "OsUpdateOptions",
    "OsVersions",
    "PortalSettings",
    "PortalSettingsStartTrigger",
    "PortalSettingsStartTriggerPort",
    "PortalSettingsStartTriggerSignal",
    "Query",
    "QuerySel",
    "QuerySession",
    "QueryTarget",
    "RadioStartConditions",
    "RadioStartConditionsType",
    "RadioStopConditions",
    "Read",
    "ReadConfig",
    "ReadConfigMembank",
    "ReaderFlashMemory",
    "ReaderInterfaceConnectionStatus",
    "ReaderInterfaceConnectionStatusDataItem",
    "ReaderInterfaceConnectionStatusDataItemConnectionStatus",
    "ReaderNetwork",
    "ReaderStats",
    "ReaderStatsAntennas",
    "ReaderStatsAntennas0",
    "ReaderStatsAntennas1",
    "ReaderStatsAntennas10",
    "ReaderStatsAntennas11",
    "ReaderStatsAntennas12",
    "ReaderStatsAntennas13",
    "ReaderStatsAntennas2",
    "ReaderStatsAntennas3",
    "ReaderStatsAntennas4",
    "ReaderStatsAntennas5",
    "ReaderStatsAntennas6",
    "ReaderStatsAntennas7",
    "ReaderStatsAntennas8",
    "ReaderStatsAntennas9",
    "ReaderStatsNtpType1",
    "ReaderStatsPowerNegotiation",
    "ReaderStatsPowerSource",
    "ReaderStatsRadioActivitiy",
    "ReaderStatsRadioConnection",
    "ReaderUpgradeStatus",
    "ReaderUpgradeStatusStatus",
    "ReaderUpgradeStatusUpdateProgressDetails",
    "ReaderVersion",
    "ReaderVersionModel",
    "ReaderVersionRevertBackFirmware",
    "ReadType",
    "RegionConfig",
    "RegionConfigMaxTxPowerSupported",
    "RegionConfigMinTxPowerSupported",
    "ReportFilter",
    "ReportFilterType",
    "RssiFilter",
    "Select",
    "SelectAction",
    "SelectMembank",
    "SelectTarget",
    "SetAppledColor",
    "SetAutostartUserappBody",
    "SetGpoBody",
    "SetInstallUserappBody",
    "SetInstallUserappBodyAuthenticationType",
    "SetInstallUserappBodyOptions",
    "SetNameAndDescription",
    "SetNTPServer",
    "SetRefreshCertificateBody",
    "SetRefreshCertificateBodyType",
    "SetReqToUserappBody",
    "SetReqToUserappResponse200",
    "SetTimeZone",
    "SetTimeZoneTimeZone",
    "SetUpdateCertificate",
    "SetUpdateCertificateAuthenticationType",
    "SetUpdateCertificateHeaders",
    "SetUpdateCertificateOptions",
    "SetUpdateCertificateType",
    "Start",
    "SupportedStandardList",
    "SupportedStandardlist",
    "SupportedStandardListRegion",
    "SupportedStandardlistSupportedStandardsItem",
    "TagDataEventsBatchingConfiguration",
    "TagDataEventsRetentionConfiguration",
    "TagIdFilter",
    "TagIdFilterMatch",
    "TagIdFilterOperation",
    "TagMetaDataV1Item",
    "TCPIP",
    "TCPIPSecurity",
    "Websocket",
    "WebsocketSecurity",
    "Write",
    "WriteConfig",
    "WriteConfigMembank",
    "WriteType",
)
