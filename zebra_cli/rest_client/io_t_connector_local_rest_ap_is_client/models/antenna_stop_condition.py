from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.antenna_stop_condition_type import AntennaStopConditionType
from ..models.antenna_stop_condition_type import check_antenna_stop_condition_type
from typing import cast
from typing import cast, Union

if TYPE_CHECKING:
  from ..models.gpi import Gpi





T = TypeVar("T", bound="AntennaStopCondition")



@_attrs_define
class AntennaStopCondition:
    """ 
        Attributes:
            type_ (AntennaStopConditionType): Type of Stop Condition
            value (Union['Gpi', float]): Value dependent on type
     """

    type_: AntennaStopConditionType
    value: Union['Gpi', float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.gpi import Gpi
        type_: str = self.type_

        value: Union[dict[str, Any], float]
        if isinstance(self.value, Gpi):
            value = self.value.to_dict()
        else:
            value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gpi import Gpi
        d = dict(src_dict)
        type_ = check_antenna_stop_condition_type(d.pop("type"))




        def _parse_value(data: object) -> Union['Gpi', float]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_1 = Gpi.from_dict(data)



                return value_type_1
            except: # noqa: E722
                pass
            return cast(Union['Gpi', float], data)

        value = _parse_value(d.pop("value"))


        antenna_stop_condition = cls(
            type_=type_,
            value=value,
        )


        antenna_stop_condition.additional_properties = d
        return antenna_stop_condition

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
