from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.tag_id_filter_match import check_tag_id_filter_match
from ..models.tag_id_filter_match import TagIdFilterMatch
from ..models.tag_id_filter_operation import check_tag_id_filter_operation
from ..models.tag_id_filter_operation import TagIdFilterOperation
from typing import cast






T = TypeVar("T", bound="TagIdFilter")



@_attrs_define
class TagIdFilter:
    """ Represents filter on the tag id.

    If absent, no filter is used.

        Attributes:
            value (str): The value to match.


                For prefix and suffix filters. Only hex digits are allowed and there must be an even number of hex digits.

                When prefix filter is used, selects cannot be used.

                For regex filter, C++ STL regex values should be used. Example: [a-zA-Z0-9]{2,}.
            match (TagIdFilterMatch): The segment or method of the id to match. Example: regex.
            operation (TagIdFilterOperation): The filter operation (include/exclude). Default: 'include'. Example: include.
     """

    value: str
    match: TagIdFilterMatch
    operation: TagIdFilterOperation = 'include'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        value = self.value

        match: str = self.match

        operation: str = self.operation


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
            "match": match,
            "operation": operation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        match = check_tag_id_filter_match(d.pop("match"))




        operation = check_tag_id_filter_operation(d.pop("operation"))




        tag_id_filter = cls(
            value=value,
            match=match,
            operation=operation,
        )


        tag_id_filter.additional_properties = d
        return tag_id_filter

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
