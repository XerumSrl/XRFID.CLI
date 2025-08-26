from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="OsVersions")



@_attrs_define
class OsVersions:
    """ 
        Attributes:
            version (Union[Unset, str]):  Example: 3.1.12.
            release_date (Union[Unset, datetime.date]):  Example: 2020-04-23.
            release_notes_url (Union[Unset, str]):  Example: https://www.zebra.com/content/dam/zebra_new_ia/en-
                us/software/operating-system/fx7500-series-operating-system/FXSeries_3_1_12_Release_Notes.pdf.
     """

    version: Union[Unset, str] = UNSET
    release_date: Union[Unset, datetime.date] = UNSET
    release_notes_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        version = self.version

        release_date: Union[Unset, str] = UNSET
        if not isinstance(self.release_date, Unset):
            release_date = self.release_date.isoformat()

        release_notes_url = self.release_notes_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if version is not UNSET:
            field_dict["version"] = version
        if release_date is not UNSET:
            field_dict["releaseDate"] = release_date
        if release_notes_url is not UNSET:
            field_dict["releaseNotesUrl"] = release_notes_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        version = d.pop("version", UNSET)

        _release_date = d.pop("releaseDate", UNSET)
        release_date: Union[Unset, datetime.date]
        if isinstance(_release_date,  Unset):
            release_date = UNSET
        else:
            release_date = isoparse(_release_date).date()




        release_notes_url = d.pop("releaseNotesUrl", UNSET)

        os_versions = cls(
            version=version,
            release_date=release_date,
            release_notes_url=release_notes_url,
        )


        os_versions.additional_properties = d
        return os_versions

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
