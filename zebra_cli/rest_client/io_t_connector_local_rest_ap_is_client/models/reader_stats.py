from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reader_stats_ntp_type_1 import check_reader_stats_ntp_type_1
from ..models.reader_stats_ntp_type_1 import ReaderStatsNtpType1
from ..models.reader_stats_power_negotiation import check_reader_stats_power_negotiation
from ..models.reader_stats_power_negotiation import ReaderStatsPowerNegotiation
from ..models.reader_stats_power_source import check_reader_stats_power_source
from ..models.reader_stats_power_source import ReaderStatsPowerSource
from ..models.reader_stats_radio_activitiy import check_reader_stats_radio_activitiy
from ..models.reader_stats_radio_activitiy import ReaderStatsRadioActivitiy
from ..models.reader_stats_radio_connection import check_reader_stats_radio_connection
from ..models.reader_stats_radio_connection import ReaderStatsRadioConnection
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, Union
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.reader_interface_connection_status import ReaderInterfaceConnectionStatus
  from ..models.memory_stats import MemoryStats
  from ..models.ntpstats import Ntpstats
  from ..models.reader_flash_memory import ReaderFlashMemory
  from ..models.cpu_stats import CpuStats
  from ..models.reader_stats_antennas import ReaderStatsAntennas





T = TypeVar("T", bound="ReaderStats")



@_attrs_define
class ReaderStats:
    """ Reader statistics information

        Attributes:
            uptime (str): Duration the reader has been powered on Example: 26 days 01:11:17.
            system_time (datetime.datetime): ISO 8601 formatted time on the reader Example: 2020-01-08T15:36:53+00:00.
            ram (MemoryStats): System memory statistics
            flash (ReaderFlashMemory): Non-volatile reader flash partitions and their usage information
            cpu (CpuStats): System CPU Statistics
            radio_connection (ReaderStatsRadioConnection): The status of the radio connection Example: connected.
            temperature (int): Current Reader Temperature (in degrees centigrade) Example: 31.
            radio_activitiy (ReaderStatsRadioActivitiy): Status of the radio activity
            power_source (ReaderStatsPowerSource): The source of power for the reader
            power_negotiation (ReaderStatsPowerNegotiation): How the power supplied to the reader is negotiated
                Only present if powerSource is POE or POE+
            ntp (Union['Ntpstats', ReaderStatsNtpType1]): NTP Configuration
            antennas (Union[Unset, ReaderStatsAntennas]): Status of the antennas connection
            interface_connection_status (Union[Unset, ReaderInterfaceConnectionStatus]): Data interface connection status
     """

    uptime: str
    system_time: datetime.datetime
    ram: 'MemoryStats'
    flash: 'ReaderFlashMemory'
    cpu: 'CpuStats'
    radio_connection: ReaderStatsRadioConnection
    temperature: int
    radio_activitiy: ReaderStatsRadioActivitiy
    power_source: ReaderStatsPowerSource
    power_negotiation: ReaderStatsPowerNegotiation
    ntp: Union['Ntpstats', ReaderStatsNtpType1]
    antennas: Union[Unset, 'ReaderStatsAntennas'] = UNSET
    interface_connection_status: Union[Unset, 'ReaderInterfaceConnectionStatus'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.reader_interface_connection_status import ReaderInterfaceConnectionStatus
        from ..models.memory_stats import MemoryStats
        from ..models.ntpstats import Ntpstats
        from ..models.reader_flash_memory import ReaderFlashMemory
        from ..models.cpu_stats import CpuStats
        from ..models.reader_stats_antennas import ReaderStatsAntennas
        uptime = self.uptime

        system_time = self.system_time.isoformat()

        ram = self.ram.to_dict()

        flash = self.flash.to_dict()

        cpu = self.cpu.to_dict()

        radio_connection: str = self.radio_connection

        temperature = self.temperature

        radio_activitiy: str = self.radio_activitiy

        power_source: str = self.power_source

        power_negotiation: str = self.power_negotiation

        ntp: Union[dict[str, Any], str]
        if isinstance(self.ntp, Ntpstats):
            ntp = self.ntp.to_dict()
        else:
            ntp = self.ntp


        antennas: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.antennas, Unset):
            antennas = self.antennas.to_dict()

        interface_connection_status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interface_connection_status, Unset):
            interface_connection_status = self.interface_connection_status.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "uptime": uptime,
            "systemTime": system_time,
            "ram": ram,
            "flash": flash,
            "cpu": cpu,
            "radioConnection": radio_connection,
            "temperature": temperature,
            "radioActivitiy": radio_activitiy,
            "powerSource": power_source,
            "powerNegotiation": power_negotiation,
            "ntp": ntp,
        })
        if antennas is not UNSET:
            field_dict["antennas"] = antennas
        if interface_connection_status is not UNSET:
            field_dict["interfaceConnectionStatus"] = interface_connection_status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reader_interface_connection_status import ReaderInterfaceConnectionStatus
        from ..models.memory_stats import MemoryStats
        from ..models.ntpstats import Ntpstats
        from ..models.reader_flash_memory import ReaderFlashMemory
        from ..models.cpu_stats import CpuStats
        from ..models.reader_stats_antennas import ReaderStatsAntennas
        d = dict(src_dict)
        uptime = d.pop("uptime")

        system_time = isoparse(d.pop("systemTime"))




        ram = MemoryStats.from_dict(d.pop("ram"))




        flash = ReaderFlashMemory.from_dict(d.pop("flash"))




        cpu = CpuStats.from_dict(d.pop("cpu"))




        radio_connection = check_reader_stats_radio_connection(d.pop("radioConnection"))




        temperature = d.pop("temperature")

        radio_activitiy = check_reader_stats_radio_activitiy(d.pop("radioActivitiy"))




        power_source = check_reader_stats_power_source(d.pop("powerSource"))




        power_negotiation = check_reader_stats_power_negotiation(d.pop("powerNegotiation"))




        def _parse_ntp(data: object) -> Union['Ntpstats', ReaderStatsNtpType1]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ntp_type_0 = Ntpstats.from_dict(data)



                return ntp_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            ntp_type_1 = check_reader_stats_ntp_type_1(data)



            return ntp_type_1

        ntp = _parse_ntp(d.pop("ntp"))


        _antennas = d.pop("antennas", UNSET)
        antennas: Union[Unset, ReaderStatsAntennas]
        if isinstance(_antennas,  Unset):
            antennas = UNSET
        else:
            antennas = ReaderStatsAntennas.from_dict(_antennas)




        _interface_connection_status = d.pop("interfaceConnectionStatus", UNSET)
        interface_connection_status: Union[Unset, ReaderInterfaceConnectionStatus]
        if isinstance(_interface_connection_status,  Unset):
            interface_connection_status = UNSET
        else:
            interface_connection_status = ReaderInterfaceConnectionStatus.from_dict(_interface_connection_status)




        reader_stats = cls(
            uptime=uptime,
            system_time=system_time,
            ram=ram,
            flash=flash,
            cpu=cpu,
            radio_connection=radio_connection,
            temperature=temperature,
            radio_activitiy=radio_activitiy,
            power_source=power_source,
            power_negotiation=power_negotiation,
            ntp=ntp,
            antennas=antennas,
            interface_connection_status=interface_connection_status,
        )


        reader_stats.additional_properties = d
        return reader_stats

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
