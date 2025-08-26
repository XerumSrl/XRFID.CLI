from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reader_version_model import check_reader_version_model
from ..models.reader_version_model import ReaderVersionModel
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.reader_version_revert_back_firmware import ReaderVersionRevertBackFirmware
  from ..models.os_versions import OsVersions





T = TypeVar("T", bound="ReaderVersion")



@_attrs_define
class ReaderVersion:
    """ Reader version information

        Attributes:
            reader_application (str): Reader software version Example: 2.7.19.0.
            radio_api (str): API to the radio engine Example: 2.2.8.2.
            radio_firmware (str): Firmware running on the radio Example: 2.1.14.0.
            radio_control_application (str): Reader radio control version Example: 1.0.0.
            reader_os (str): Reader operating system version Example: 2.2.15.0.
            reader_hardware (str): Hardware version of the reader Example: 0.0.5.0.
            reader_boot_loader (str): Reader boot loader version Example: 2.1.2.0.
            reader_file_system (str): Reader root file system version Example: 2.1.2.0.
            cloud_agent_application (str): Reader cloud agent version Example: 1.0.0.
            available_os_upgrades (list['OsVersions']): A List of available OS upgrades, (upgrade path only, no downgrade
                versions) Example: [ 3.1.12, 3.0.35 ].
            model (ReaderVersionModel): device model
            serial_number (str): Device serial number Example: 84248dee5721.
            revert_back_firmware (ReaderVersionRevertBackFirmware): current revertback firmware details
            fpga (Union[Unset, str]): FPGA running on radio (only applicable to ATR7000) Example: 1.8.0.0.
     """

    reader_application: str
    radio_api: str
    radio_firmware: str
    radio_control_application: str
    reader_os: str
    reader_hardware: str
    reader_boot_loader: str
    reader_file_system: str
    cloud_agent_application: str
    available_os_upgrades: list['OsVersions']
    model: ReaderVersionModel
    serial_number: str
    revert_back_firmware: 'ReaderVersionRevertBackFirmware'
    fpga: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.reader_version_revert_back_firmware import ReaderVersionRevertBackFirmware
        from ..models.os_versions import OsVersions
        reader_application = self.reader_application

        radio_api = self.radio_api

        radio_firmware = self.radio_firmware

        radio_control_application = self.radio_control_application

        reader_os = self.reader_os

        reader_hardware = self.reader_hardware

        reader_boot_loader = self.reader_boot_loader

        reader_file_system = self.reader_file_system

        cloud_agent_application = self.cloud_agent_application

        available_os_upgrades = []
        for available_os_upgrades_item_data in self.available_os_upgrades:
            available_os_upgrades_item = available_os_upgrades_item_data.to_dict()
            available_os_upgrades.append(available_os_upgrades_item)



        model: str = self.model

        serial_number = self.serial_number

        revert_back_firmware = self.revert_back_firmware.to_dict()

        fpga = self.fpga


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "readerApplication": reader_application,
            "radioApi": radio_api,
            "radioFirmware": radio_firmware,
            "radioControlApplication": radio_control_application,
            "readerOS": reader_os,
            "readerHardware": reader_hardware,
            "readerBootLoader": reader_boot_loader,
            "readerFileSystem": reader_file_system,
            "cloudAgentApplication": cloud_agent_application,
            "availableOsUpgrades": available_os_upgrades,
            "model": model,
            "serialNumber": serial_number,
            "revertBackFirmware": revert_back_firmware,
        })
        if fpga is not UNSET:
            field_dict["fpga"] = fpga

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reader_version_revert_back_firmware import ReaderVersionRevertBackFirmware
        from ..models.os_versions import OsVersions
        d = dict(src_dict)
        reader_application = d.pop("readerApplication")

        radio_api = d.pop("radioApi")

        radio_firmware = d.pop("radioFirmware")

        radio_control_application = d.pop("radioControlApplication")

        reader_os = d.pop("readerOS")

        reader_hardware = d.pop("readerHardware")

        reader_boot_loader = d.pop("readerBootLoader")

        reader_file_system = d.pop("readerFileSystem")

        cloud_agent_application = d.pop("cloudAgentApplication")

        available_os_upgrades = []
        _available_os_upgrades = d.pop("availableOsUpgrades")
        for available_os_upgrades_item_data in (_available_os_upgrades):
            available_os_upgrades_item = OsVersions.from_dict(available_os_upgrades_item_data)



            available_os_upgrades.append(available_os_upgrades_item)


        model = check_reader_version_model(d.pop("model"))




        serial_number = d.pop("serialNumber")

        revert_back_firmware = ReaderVersionRevertBackFirmware.from_dict(d.pop("revertBackFirmware"))




        fpga = d.pop("fpga", UNSET)

        reader_version = cls(
            reader_application=reader_application,
            radio_api=radio_api,
            radio_firmware=radio_firmware,
            radio_control_application=radio_control_application,
            reader_os=reader_os,
            reader_hardware=reader_hardware,
            reader_boot_loader=reader_boot_loader,
            reader_file_system=reader_file_system,
            cloud_agent_application=cloud_agent_application,
            available_os_upgrades=available_os_upgrades,
            model=model,
            serial_number=serial_number,
            revert_back_firmware=revert_back_firmware,
            fpga=fpga,
        )


        reader_version.additional_properties = d
        return reader_version

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
