from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.action_conditions_v1_type_1_operator import ActionConditionsV1Type1Operator
from ..models.action_conditions_v1_type_1_operator import check_action_conditions_v1_type_1_operator
from ..models.conditions_array_v1_item import check_conditions_array_v1_item
from ..models.conditions_array_v1_item import ConditionsArrayV1Item
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="ActionConditionsV1Type1")



@_attrs_define
class ActionConditionsV1Type1:
    """ 
        Attributes:
            operator (Union[Unset, ActionConditionsV1Type1Operator]): operator tobe used for conditions validation
            operands (Union[Unset, list[ConditionsArrayV1Item]]): Predefined conditions

                IS_CLOUD_CONNECTED  : Condition will be true when reader is successfully connected to Cloud.

                ~IS_CLOUD_CONNECTED : Condition will be true when reader lost Cloud connectivity.

                IS_RADIO_ONGOING    : Condition will be true when reader is currenty performing inventory or started inventory
                operation.

                ~IS_RADIO_ONGOING   : Condition will be true when reader is not performing inventory or stoped inventory
                operation.
     """

    operator: Union[Unset, ActionConditionsV1Type1Operator] = UNSET
    operands: Union[Unset, list[ConditionsArrayV1Item]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        operator: Union[Unset, str] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator


        operands: Union[Unset, list[str]] = UNSET
        if not isinstance(self.operands, Unset):
            operands = []
            for componentsschemasconditions_array_v_1_item_data in self.operands:
                componentsschemasconditions_array_v_1_item: str = componentsschemasconditions_array_v_1_item_data
                operands.append(componentsschemasconditions_array_v_1_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if operator is not UNSET:
            field_dict["operator"] = operator
        if operands is not UNSET:
            field_dict["operands"] = operands

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, ActionConditionsV1Type1Operator]
        if isinstance(_operator,  Unset):
            operator = UNSET
        else:
            operator = check_action_conditions_v1_type_1_operator(_operator)




        operands = []
        _operands = d.pop("operands", UNSET)
        for componentsschemasconditions_array_v_1_item_data in (_operands or []):
            componentsschemasconditions_array_v_1_item = check_conditions_array_v1_item(componentsschemasconditions_array_v_1_item_data)



            operands.append(componentsschemasconditions_array_v_1_item)


        action_conditions_v1_type_1 = cls(
            operator=operator,
            operands=operands,
        )


        action_conditions_v1_type_1.additional_properties = d
        return action_conditions_v1_type_1

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
