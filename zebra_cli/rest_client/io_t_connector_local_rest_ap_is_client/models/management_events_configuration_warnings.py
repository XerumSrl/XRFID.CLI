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
  from ..models.management_events_configuration_warnings_userapp import ManagementEventsConfigurationWarningsUserapp
  from ..models.management_events_configuration_warnings_ram import ManagementEventsConfigurationWarningsRam
  from ..models.management_events_configuration_warnings_temperature import ManagementEventsConfigurationWarningsTemperature
  from ..models.management_events_configuration_warnings_flash import ManagementEventsConfigurationWarningsFlash
  from ..models.management_events_configuration_warnings_cpu import ManagementEventsConfigurationWarningsCpu
  from ..models.management_events_configuration_warnings_ntp_type_0 import ManagementEventsConfigurationWarningsNtpType0





T = TypeVar("T", bound="ManagementEventsConfigurationWarnings")



@_attrs_define
class ManagementEventsConfigurationWarnings:
    """ Asynchronous Management Warnings

        Attributes:
            cpu (Union[Unset, ManagementEventsConfigurationWarningsCpu]): CPU Usage Warning Alerts
            flash (Union[Unset, ManagementEventsConfigurationWarningsFlash]): Flash Usage Warning Alerts
            ram (Union[Unset, ManagementEventsConfigurationWarningsRam]): RAM Usage Warning Alerts
            ntp (Union['ManagementEventsConfigurationWarningsNtpType0', Unset, bool]): NTP Warning Alert
            temperature (Union[Unset, ManagementEventsConfigurationWarningsTemperature]): Reader temperature warning limits
            database (Union[Unset, bool]): Radio Database warnings Default: True.
            radio_api (Union[Unset, bool]): NGE warnings Default: True.
            radio_control (Union[Unset, bool]): Radio Control warnings Default: True.
            reader_gateway (Union[Unset, bool]): Reader Gateway Errors Default: True.
            userapp (Union[Unset, ManagementEventsConfigurationWarningsUserapp]):
     """

    cpu: Union[Unset, 'ManagementEventsConfigurationWarningsCpu'] = UNSET
    flash: Union[Unset, 'ManagementEventsConfigurationWarningsFlash'] = UNSET
    ram: Union[Unset, 'ManagementEventsConfigurationWarningsRam'] = UNSET
    ntp: Union['ManagementEventsConfigurationWarningsNtpType0', Unset, bool] = UNSET
    temperature: Union[Unset, 'ManagementEventsConfigurationWarningsTemperature'] = UNSET
    database: Union[Unset, bool] = True
    radio_api: Union[Unset, bool] = True
    radio_control: Union[Unset, bool] = True
    reader_gateway: Union[Unset, bool] = True
    userapp: Union[Unset, 'ManagementEventsConfigurationWarningsUserapp'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.management_events_configuration_warnings_userapp import ManagementEventsConfigurationWarningsUserapp
        from ..models.management_events_configuration_warnings_ram import ManagementEventsConfigurationWarningsRam
        from ..models.management_events_configuration_warnings_temperature import ManagementEventsConfigurationWarningsTemperature
        from ..models.management_events_configuration_warnings_flash import ManagementEventsConfigurationWarningsFlash
        from ..models.management_events_configuration_warnings_cpu import ManagementEventsConfigurationWarningsCpu
        from ..models.management_events_configuration_warnings_ntp_type_0 import ManagementEventsConfigurationWarningsNtpType0
        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        flash: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.flash, Unset):
            flash = self.flash.to_dict()

        ram: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.ram, Unset):
            ram = self.ram.to_dict()

        ntp: Union[Unset, bool, dict[str, Any]]
        if isinstance(self.ntp, Unset):
            ntp = UNSET
        elif isinstance(self.ntp, ManagementEventsConfigurationWarningsNtpType0):
            ntp = self.ntp.to_dict()
        else:
            ntp = self.ntp

        temperature: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.temperature, Unset):
            temperature = self.temperature.to_dict()

        database = self.database

        radio_api = self.radio_api

        radio_control = self.radio_control

        reader_gateway = self.reader_gateway

        userapp: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.userapp, Unset):
            userapp = self.userapp.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if flash is not UNSET:
            field_dict["flash"] = flash
        if ram is not UNSET:
            field_dict["ram"] = ram
        if ntp is not UNSET:
            field_dict["ntp"] = ntp
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if database is not UNSET:
            field_dict["database"] = database
        if radio_api is not UNSET:
            field_dict["radio_api"] = radio_api
        if radio_control is not UNSET:
            field_dict["radio_control"] = radio_control
        if reader_gateway is not UNSET:
            field_dict["reader_gateway"] = reader_gateway
        if userapp is not UNSET:
            field_dict["userapp"] = userapp

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.management_events_configuration_warnings_userapp import ManagementEventsConfigurationWarningsUserapp
        from ..models.management_events_configuration_warnings_ram import ManagementEventsConfigurationWarningsRam
        from ..models.management_events_configuration_warnings_temperature import ManagementEventsConfigurationWarningsTemperature
        from ..models.management_events_configuration_warnings_flash import ManagementEventsConfigurationWarningsFlash
        from ..models.management_events_configuration_warnings_cpu import ManagementEventsConfigurationWarningsCpu
        from ..models.management_events_configuration_warnings_ntp_type_0 import ManagementEventsConfigurationWarningsNtpType0
        d = dict(src_dict)
        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, ManagementEventsConfigurationWarningsCpu]
        if isinstance(_cpu,  Unset):
            cpu = UNSET
        else:
            cpu = ManagementEventsConfigurationWarningsCpu.from_dict(_cpu)




        _flash = d.pop("flash", UNSET)
        flash: Union[Unset, ManagementEventsConfigurationWarningsFlash]
        if isinstance(_flash,  Unset):
            flash = UNSET
        else:
            flash = ManagementEventsConfigurationWarningsFlash.from_dict(_flash)




        _ram = d.pop("ram", UNSET)
        ram: Union[Unset, ManagementEventsConfigurationWarningsRam]
        if isinstance(_ram,  Unset):
            ram = UNSET
        else:
            ram = ManagementEventsConfigurationWarningsRam.from_dict(_ram)




        def _parse_ntp(data: object) -> Union['ManagementEventsConfigurationWarningsNtpType0', Unset, bool]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ntp_type_0 = ManagementEventsConfigurationWarningsNtpType0.from_dict(data)



                return ntp_type_0
            except: # noqa: E722
                pass
            return cast(Union['ManagementEventsConfigurationWarningsNtpType0', Unset, bool], data)

        ntp = _parse_ntp(d.pop("ntp", UNSET))


        _temperature = d.pop("temperature", UNSET)
        temperature: Union[Unset, ManagementEventsConfigurationWarningsTemperature]
        if isinstance(_temperature,  Unset):
            temperature = UNSET
        else:
            temperature = ManagementEventsConfigurationWarningsTemperature.from_dict(_temperature)




        database = d.pop("database", UNSET)

        radio_api = d.pop("radio_api", UNSET)

        radio_control = d.pop("radio_control", UNSET)

        reader_gateway = d.pop("reader_gateway", UNSET)

        _userapp = d.pop("userapp", UNSET)
        userapp: Union[Unset, ManagementEventsConfigurationWarningsUserapp]
        if isinstance(_userapp,  Unset):
            userapp = UNSET
        else:
            userapp = ManagementEventsConfigurationWarningsUserapp.from_dict(_userapp)




        management_events_configuration_warnings = cls(
            cpu=cpu,
            flash=flash,
            ram=ram,
            ntp=ntp,
            temperature=temperature,
            database=database,
            radio_api=radio_api,
            radio_control=radio_control,
            reader_gateway=reader_gateway,
            userapp=userapp,
        )


        management_events_configuration_warnings.additional_properties = d
        return management_events_configuration_warnings

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
