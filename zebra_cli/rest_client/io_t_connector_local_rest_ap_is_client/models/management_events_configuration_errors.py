from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.management_events_configuration_errors_flash import ManagementEventsConfigurationErrorsFlash
  from ..models.management_events_configuration_errors_cpu import ManagementEventsConfigurationErrorsCpu
  from ..models.management_events_configuration_errors_userapp import ManagementEventsConfigurationErrorsUserapp
  from ..models.management_events_configuration_errors_ram import ManagementEventsConfigurationErrorsRam





T = TypeVar("T", bound="ManagementEventsConfigurationErrors")



@_attrs_define
class ManagementEventsConfigurationErrors:
    """ Asynchronous Management Errors

        Attributes:
            cpu (Union[Unset, ManagementEventsConfigurationErrorsCpu]): CPU Usage Error Alerts
            flash (Union[Unset, ManagementEventsConfigurationErrorsFlash]): Flash Usage Error Alerts
            ram (Union[Unset, ManagementEventsConfigurationErrorsRam]): RAM Usage Error Alerts
            reader_gateway (Union[Unset, bool]): Reader Gateway Errors Default: True.
            antenna (Union[Unset, bool]): Antenna Connect/Disconnect Alerts Default: True.
            database (Union[Unset, bool]): Radio Database Error Alerts Default: True.
            radio (Union[Unset, bool]): Radio Error Alerts Default: True.
            radio_control (Union[Unset, bool]): Radio Control Error Alerts Default: True.
            userapp (Union[Unset, ManagementEventsConfigurationErrorsUserapp]):
     """

    cpu: Union[Unset, 'ManagementEventsConfigurationErrorsCpu'] = UNSET
    flash: Union[Unset, 'ManagementEventsConfigurationErrorsFlash'] = UNSET
    ram: Union[Unset, 'ManagementEventsConfigurationErrorsRam'] = UNSET
    reader_gateway: Union[Unset, bool] = True
    antenna: Union[Unset, bool] = True
    database: Union[Unset, bool] = True
    radio: Union[Unset, bool] = True
    radio_control: Union[Unset, bool] = True
    userapp: Union[Unset, 'ManagementEventsConfigurationErrorsUserapp'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.management_events_configuration_errors_flash import ManagementEventsConfigurationErrorsFlash
        from ..models.management_events_configuration_errors_cpu import ManagementEventsConfigurationErrorsCpu
        from ..models.management_events_configuration_errors_userapp import ManagementEventsConfigurationErrorsUserapp
        from ..models.management_events_configuration_errors_ram import ManagementEventsConfigurationErrorsRam
        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        flash: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.flash, Unset):
            flash = self.flash.to_dict()

        ram: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.ram, Unset):
            ram = self.ram.to_dict()

        reader_gateway = self.reader_gateway

        antenna = self.antenna

        database = self.database

        radio = self.radio

        radio_control = self.radio_control

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
        if reader_gateway is not UNSET:
            field_dict["reader_gateway"] = reader_gateway
        if antenna is not UNSET:
            field_dict["antenna"] = antenna
        if database is not UNSET:
            field_dict["database"] = database
        if radio is not UNSET:
            field_dict["radio"] = radio
        if radio_control is not UNSET:
            field_dict["radio_control"] = radio_control
        if userapp is not UNSET:
            field_dict["userapp"] = userapp

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.management_events_configuration_errors_flash import ManagementEventsConfigurationErrorsFlash
        from ..models.management_events_configuration_errors_cpu import ManagementEventsConfigurationErrorsCpu
        from ..models.management_events_configuration_errors_userapp import ManagementEventsConfigurationErrorsUserapp
        from ..models.management_events_configuration_errors_ram import ManagementEventsConfigurationErrorsRam
        d = dict(src_dict)
        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, ManagementEventsConfigurationErrorsCpu]
        if isinstance(_cpu,  Unset):
            cpu = UNSET
        else:
            cpu = ManagementEventsConfigurationErrorsCpu.from_dict(_cpu)




        _flash = d.pop("flash", UNSET)
        flash: Union[Unset, ManagementEventsConfigurationErrorsFlash]
        if isinstance(_flash,  Unset):
            flash = UNSET
        else:
            flash = ManagementEventsConfigurationErrorsFlash.from_dict(_flash)




        _ram = d.pop("ram", UNSET)
        ram: Union[Unset, ManagementEventsConfigurationErrorsRam]
        if isinstance(_ram,  Unset):
            ram = UNSET
        else:
            ram = ManagementEventsConfigurationErrorsRam.from_dict(_ram)




        reader_gateway = d.pop("reader_gateway", UNSET)

        antenna = d.pop("antenna", UNSET)

        database = d.pop("database", UNSET)

        radio = d.pop("radio", UNSET)

        radio_control = d.pop("radio_control", UNSET)

        _userapp = d.pop("userapp", UNSET)
        userapp: Union[Unset, ManagementEventsConfigurationErrorsUserapp]
        if isinstance(_userapp,  Unset):
            userapp = UNSET
        else:
            userapp = ManagementEventsConfigurationErrorsUserapp.from_dict(_userapp)




        management_events_configuration_errors = cls(
            cpu=cpu,
            flash=flash,
            ram=ram,
            reader_gateway=reader_gateway,
            antenna=antenna,
            database=database,
            radio=radio,
            radio_control=radio_control,
            userapp=userapp,
        )


        management_events_configuration_errors.additional_properties = d
        return management_events_configuration_errors

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
