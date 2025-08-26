from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.radio_start_conditions_type import check_radio_start_conditions_type
from ..models.radio_start_conditions_type import RadioStartConditionsType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.gpi import Gpi





T = TypeVar("T", bound="RadioStartConditions")



@_attrs_define
class RadioStartConditions:
    """ Controls when, after a “start” is issued, the radio starts trying to inventory tags.

    If absent, the radio will immediately begin inventorying tags upon a "start" command.

        Attributes:
            type_ (Union[Unset, RadioStartConditionsType]):
            gpis (Union[Unset, list['Gpi']]):
     """

    type_: Union[Unset, RadioStartConditionsType] = UNSET
    gpis: Union[Unset, list['Gpi']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.gpi import Gpi
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_


        gpis: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.gpis, Unset):
            gpis = []
            for gpis_item_data in self.gpis:
                gpis_item = gpis_item_data.to_dict()
                gpis.append(gpis_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if gpis is not UNSET:
            field_dict["gpis"] = gpis

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gpi import Gpi
        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, RadioStartConditionsType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = check_radio_start_conditions_type(_type_)




        gpis = []
        _gpis = d.pop("gpis", UNSET)
        for gpis_item_data in (_gpis or []):
            gpis_item = Gpi.from_dict(gpis_item_data)



            gpis.append(gpis_item)


        radio_start_conditions = cls(
            type_=type_,
            gpis=gpis,
        )


        radio_start_conditions.additional_properties = d
        return radio_start_conditions

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
