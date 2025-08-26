from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.conditions_array_v1_item import check_conditions_array_v1_item
from ..models.conditions_array_v1_item import ConditionsArrayV1Item
from ..models.gpo_action_pin import check_gpo_action_pin
from ..models.gpo_action_pin import GPOActionPin
from ..models.gpo_action_post_action_state import check_gpo_action_post_action_state
from ..models.gpo_action_post_action_state import GPOActionPostActionState
from ..models.gpo_action_state import check_gpo_action_state
from ..models.gpo_action_state import GPOActionState
from ..models.gpo_action_type import check_gpo_action_type
from ..models.gpo_action_type import GPOActionType
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.action_blink_configuration import ActionBlinkConfiguration
  from ..models.action_conditions_v1_type_1 import ActionConditionsV1Type1





T = TypeVar("T", bound="GPOAction")



@_attrs_define
class GPOAction:
    """ Configuration to define operations on single GPO.

    GPO Action will be skipped if conditions provided is not satisfied.

        Attributes:
            type_ (GPOActionType): Action type
            pin (GPOActionPin): GPO pin number Example: 1.
            state (GPOActionState): Desired GPO pin state
            post_action_state (Union[Unset, GPOActionPostActionState]): Desired GPO pin state after action execution
                completed
            blink (Union[Unset, ActionBlinkConfiguration]): action blink configuration for GPO or LED
            conditions (Union['ActionConditionsV1Type1', Unset, list[ConditionsArrayV1Item]]): Predefined conditions to
                trigger GPO or LED actions

                Default "and" operator is used when array of conditions is provided.

                operator "and": Action is performed only when all the conditions provided is true.
                operator "or": Action is performed only when one of the conditions provided is true.
     """

    type_: GPOActionType
    pin: GPOActionPin
    state: GPOActionState
    post_action_state: Union[Unset, GPOActionPostActionState] = UNSET
    blink: Union[Unset, 'ActionBlinkConfiguration'] = UNSET
    conditions: Union['ActionConditionsV1Type1', Unset, list[ConditionsArrayV1Item]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.action_blink_configuration import ActionBlinkConfiguration
        from ..models.action_conditions_v1_type_1 import ActionConditionsV1Type1
        type_: str = self.type_

        pin: int = self.pin

        state: str = self.state

        post_action_state: Union[Unset, str] = UNSET
        if not isinstance(self.post_action_state, Unset):
            post_action_state = self.post_action_state


        blink: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.blink, Unset):
            blink = self.blink.to_dict()

        conditions: Union[Unset, dict[str, Any], list[str]]
        if isinstance(self.conditions, Unset):
            conditions = UNSET
        elif isinstance(self.conditions, list):
            conditions = []
            for componentsschemasconditions_array_v_1_item_data in self.conditions:
                componentsschemasconditions_array_v_1_item: str = componentsschemasconditions_array_v_1_item_data
                conditions.append(componentsschemasconditions_array_v_1_item)


        else:
            conditions = self.conditions.to_dict()



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "pin": pin,
            "state": state,
        })
        if post_action_state is not UNSET:
            field_dict["postActionState"] = post_action_state
        if blink is not UNSET:
            field_dict["blink"] = blink
        if conditions is not UNSET:
            field_dict["conditions"] = conditions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action_blink_configuration import ActionBlinkConfiguration
        from ..models.action_conditions_v1_type_1 import ActionConditionsV1Type1
        d = dict(src_dict)
        type_ = check_gpo_action_type(d.pop("type"))




        pin = check_gpo_action_pin(d.pop("pin"))




        state = check_gpo_action_state(d.pop("state"))




        _post_action_state = d.pop("postActionState", UNSET)
        post_action_state: Union[Unset, GPOActionPostActionState]
        if isinstance(_post_action_state,  Unset):
            post_action_state = UNSET
        else:
            post_action_state = check_gpo_action_post_action_state(_post_action_state)




        _blink = d.pop("blink", UNSET)
        blink: Union[Unset, ActionBlinkConfiguration]
        if isinstance(_blink,  Unset):
            blink = UNSET
        else:
            blink = ActionBlinkConfiguration.from_dict(_blink)




        def _parse_conditions(data: object) -> Union['ActionConditionsV1Type1', Unset, list[ConditionsArrayV1Item]]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemasaction_conditions_v_1_type_0 = []
                _componentsschemasaction_conditions_v_1_type_0 = data
                for componentsschemasconditions_array_v_1_item_data in (_componentsschemasaction_conditions_v_1_type_0):
                    componentsschemasconditions_array_v_1_item = check_conditions_array_v1_item(componentsschemasconditions_array_v_1_item_data)



                    componentsschemasaction_conditions_v_1_type_0.append(componentsschemasconditions_array_v_1_item)

                return componentsschemasaction_conditions_v_1_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemasaction_conditions_v_1_type_1 = ActionConditionsV1Type1.from_dict(data)



            return componentsschemasaction_conditions_v_1_type_1

        conditions = _parse_conditions(d.pop("conditions", UNSET))


        gpo_action = cls(
            type_=type_,
            pin=pin,
            state=state,
            post_action_state=post_action_state,
            blink=blink,
            conditions=conditions,
        )


        gpo_action.additional_properties = d
        return gpo_action

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
