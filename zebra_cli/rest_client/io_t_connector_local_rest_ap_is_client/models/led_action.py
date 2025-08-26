from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.conditions_array_v1_item import check_conditions_array_v1_item
from ..models.conditions_array_v1_item import ConditionsArrayV1Item
from ..models.led_action_color import check_led_action_color
from ..models.led_action_color import LEDActionColor
from ..models.led_action_led import check_led_action_led
from ..models.led_action_led import LEDActionLed
from ..models.led_action_post_action_color import check_led_action_post_action_color
from ..models.led_action_post_action_color import LEDActionPostActionColor
from ..models.led_action_type import check_led_action_type
from ..models.led_action_type import LEDActionType
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.action_blink_configuration import ActionBlinkConfiguration
  from ..models.action_conditions_v1_type_1 import ActionConditionsV1Type1





T = TypeVar("T", bound="LEDAction")



@_attrs_define
class LEDAction:
    """ Configuration to define operations on single LED.

    LED Action will be skipped if conditions provided is not satisfied.

        Attributes:
            type_ (LEDActionType): Action type
            led (LEDActionLed): LED number
            color (LEDActionColor): Desired LED color
            post_action_color (Union[Unset, LEDActionPostActionColor]): Desired LED color after action expired
            blink (Union[Unset, ActionBlinkConfiguration]): action blink configuration for GPO or LED
            conditions (Union['ActionConditionsV1Type1', Unset, list[ConditionsArrayV1Item]]): Predefined conditions to
                trigger GPO or LED actions

                Default "and" operator is used when array of conditions is provided.

                operator "and": Action is performed only when all the conditions provided is true.
                operator "or": Action is performed only when one of the conditions provided is true.
     """

    type_: LEDActionType
    led: LEDActionLed
    color: LEDActionColor
    post_action_color: Union[Unset, LEDActionPostActionColor] = UNSET
    blink: Union[Unset, 'ActionBlinkConfiguration'] = UNSET
    conditions: Union['ActionConditionsV1Type1', Unset, list[ConditionsArrayV1Item]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.action_blink_configuration import ActionBlinkConfiguration
        from ..models.action_conditions_v1_type_1 import ActionConditionsV1Type1
        type_: str = self.type_

        led: int = self.led

        color: str = self.color

        post_action_color: Union[Unset, str] = UNSET
        if not isinstance(self.post_action_color, Unset):
            post_action_color = self.post_action_color


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
            "led": led,
            "color": color,
        })
        if post_action_color is not UNSET:
            field_dict["postActionColor"] = post_action_color
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
        type_ = check_led_action_type(d.pop("type"))




        led = check_led_action_led(d.pop("led"))




        color = check_led_action_color(d.pop("color"))




        _post_action_color = d.pop("postActionColor", UNSET)
        post_action_color: Union[Unset, LEDActionPostActionColor]
        if isinstance(_post_action_color,  Unset):
            post_action_color = UNSET
        else:
            post_action_color = check_led_action_post_action_color(_post_action_color)




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


        led_action = cls(
            type_=type_,
            led=led,
            color=color,
            post_action_color=post_action_color,
            blink=blink,
            conditions=conditions,
        )


        led_action.additional_properties = d
        return led_action

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
