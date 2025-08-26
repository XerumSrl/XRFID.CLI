from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reader_upgrade_status_status import check_reader_upgrade_status_status
from ..models.reader_upgrade_status_status import ReaderUpgradeStatusStatus
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.reader_upgrade_status_update_progress_details import ReaderUpgradeStatusUpdateProgressDetails





T = TypeVar("T", bound="ReaderUpgradeStatus")



@_attrs_define
class ReaderUpgradeStatus:
    """ 
        Attributes:
            status (Union[Unset, ReaderUpgradeStatusStatus]):
            image_download_progress (Union[Unset, float]): Upgrade image download percentage
            overall_update_progress (Union[Unset, float]): Overall upgrade percentage
            update_progress_details (Union[Unset, ReaderUpgradeStatusUpdateProgressDetails]):
     """

    status: Union[Unset, ReaderUpgradeStatusStatus] = UNSET
    image_download_progress: Union[Unset, float] = UNSET
    overall_update_progress: Union[Unset, float] = UNSET
    update_progress_details: Union[Unset, 'ReaderUpgradeStatusUpdateProgressDetails'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.reader_upgrade_status_update_progress_details import ReaderUpgradeStatusUpdateProgressDetails
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status


        image_download_progress = self.image_download_progress

        overall_update_progress = self.overall_update_progress

        update_progress_details: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.update_progress_details, Unset):
            update_progress_details = self.update_progress_details.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if status is not UNSET:
            field_dict["status"] = status
        if image_download_progress is not UNSET:
            field_dict["imageDownloadProgress"] = image_download_progress
        if overall_update_progress is not UNSET:
            field_dict["overallUpdateProgress"] = overall_update_progress
        if update_progress_details is not UNSET:
            field_dict["updateProgressDetails"] = update_progress_details

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reader_upgrade_status_update_progress_details import ReaderUpgradeStatusUpdateProgressDetails
        d = dict(src_dict)
        _status = d.pop("status", UNSET)
        status: Union[Unset, ReaderUpgradeStatusStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_reader_upgrade_status_status(_status)




        image_download_progress = d.pop("imageDownloadProgress", UNSET)

        overall_update_progress = d.pop("overallUpdateProgress", UNSET)

        _update_progress_details = d.pop("updateProgressDetails", UNSET)
        update_progress_details: Union[Unset, ReaderUpgradeStatusUpdateProgressDetails]
        if isinstance(_update_progress_details,  Unset):
            update_progress_details = UNSET
        else:
            update_progress_details = ReaderUpgradeStatusUpdateProgressDetails.from_dict(_update_progress_details)




        reader_upgrade_status = cls(
            status=status,
            image_download_progress=image_download_progress,
            overall_update_progress=overall_update_progress,
            update_progress_details=update_progress_details,
        )


        reader_upgrade_status.additional_properties = d
        return reader_upgrade_status

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
