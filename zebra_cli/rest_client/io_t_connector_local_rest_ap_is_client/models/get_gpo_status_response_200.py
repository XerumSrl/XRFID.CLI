from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_gpo_status_response_2001 import check_get_gpo_status_response_2001
from ..models.get_gpo_status_response_2001 import GetGpoStatusResponse2001
from ..models.get_gpo_status_response_2002 import check_get_gpo_status_response_2002
from ..models.get_gpo_status_response_2002 import GetGpoStatusResponse2002
from ..models.get_gpo_status_response_2003 import check_get_gpo_status_response_2003
from ..models.get_gpo_status_response_2003 import GetGpoStatusResponse2003
from ..models.get_gpo_status_response_2004 import check_get_gpo_status_response_2004
from ..models.get_gpo_status_response_2004 import GetGpoStatusResponse2004
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="GetGpoStatusResponse200")



@_attrs_define
class GetGpoStatusResponse200:
    """ 
        Attributes:
            1 (GetGpoStatusResponse2001): pin number and its state
            2 (GetGpoStatusResponse2002): pin number and its state
            3 (Union[Unset, GetGpoStatusResponse2003]): pin number and its state
            4 (Union[Unset, GetGpoStatusResponse2004]): pin number and its state
     """

    1: GetGpoStatusResponse2001
    2: GetGpoStatusResponse2002
    3: Union[Unset, GetGpoStatusResponse2003] = UNSET
    4: Union[Unset, GetGpoStatusResponse2004] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        1: str = self.1

        2: str = self.2

        3: Union[Unset, str] = UNSET
        if not isinstance(self.3, Unset):
            3 = self.3


        4: Union[Unset, str] = UNSET
        if not isinstance(self.4, Unset):
            4 = self.4



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "1": 1,
            "2": 2,
        })
        if 3 is not UNSET:
            field_dict["3"] = 3
        if 4 is not UNSET:
            field_dict["4"] = 4

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        1 = check_get_gpo_status_response_2001(d.pop("1"))




        2 = check_get_gpo_status_response_2002(d.pop("2"))




        _3 = d.pop("3", UNSET)
        3: Union[Unset, GetGpoStatusResponse2003]
        if isinstance(_3,  Unset):
            3 = UNSET
        else:
            3 = check_get_gpo_status_response_2003(_3)




        _4 = d.pop("4", UNSET)
        4: Union[Unset, GetGpoStatusResponse2004]
        if isinstance(_4,  Unset):
            4 = UNSET
        else:
            4 = check_get_gpo_status_response_2004(_4)




        get_gpo_status_response_200 = cls(
            1=1,
            2=2,
            3=3,
            4=4,
        )


        get_gpo_status_response_200.additional_properties = d
        return get_gpo_status_response_200

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
