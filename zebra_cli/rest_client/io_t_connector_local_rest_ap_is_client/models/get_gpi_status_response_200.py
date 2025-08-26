from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_gpi_status_response_2001 import check_get_gpi_status_response_2001
from ..models.get_gpi_status_response_2001 import GetGpiStatusResponse2001
from ..models.get_gpi_status_response_2002 import check_get_gpi_status_response_2002
from ..models.get_gpi_status_response_2002 import GetGpiStatusResponse2002
from ..models.get_gpi_status_response_2003 import check_get_gpi_status_response_2003
from ..models.get_gpi_status_response_2003 import GetGpiStatusResponse2003
from ..types import UNSET, Unset
from typing import cast
from typing import Union


T = TypeVar("T", bound="GetGpiStatusResponse200")


@_attrs_define
class GetGpiStatusResponse200:
    """ 
        Attributes:
            pin_1 (GetGpiStatusResponse2001): pin number and its state
            pin_2 (GetGpiStatusResponse2002): pin number and its state  
            pin_3 (Union[Unset, GetGpiStatusResponse2003]): pin number and its state
     """

    pin_1: GetGpiStatusResponse2001 = _attrs_field(alias="1")
    pin_2: GetGpiStatusResponse2002 = _attrs_field(alias="2")
    pin_3: Union[Unset, GetGpiStatusResponse2003] = _attrs_field(alias="3", default=UNSET)
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pin_1_value: str = self.pin_1

        pin_2_value: str = self.pin_2

        pin_3_value: Union[Unset, str] = UNSET
        if not isinstance(self.pin_3, Unset):
            pin_3_value = self.pin_3

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "1": pin_1_value,
            "2": pin_2_value,
        })
        if pin_3_value is not UNSET:
            field_dict["3"] = pin_3_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pin_1_value = check_get_gpi_status_response_2001(d.pop("1"))
        pin_2_value = check_get_gpi_status_response_2002(d.pop("2"))

        _pin_3 = d.pop("3", UNSET)
        pin_3_value: Union[Unset, GetGpiStatusResponse2003]
        if isinstance(_pin_3, Unset):
            pin_3_value = UNSET
        else:
            pin_3_value = check_get_gpi_status_response_2003(_pin_3)

        get_gpi_status_response_200 = cls(
            pin_1=pin_1_value,
            pin_2=pin_2_value,
            pin_3=pin_3_value,
        )

        get_gpi_status_response_200.additional_properties = d
        return get_gpi_status_response_200

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
