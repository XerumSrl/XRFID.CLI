from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.query_sel import check_query_sel
from ..models.query_sel import QuerySel
from ..models.query_session import check_query_session
from ..models.query_session import QuerySession
from ..models.query_target import check_query_target
from ..models.query_target import QueryTarget
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="Query")



@_attrs_define
class Query:
    """ 
        Attributes:
            tag_population (Union[Unset, int]): Expected number of tags
            sel (Union[Unset, QuerySel]): Sel field (see EPC Gen2 Spec)
            session (Union[Unset, QuerySession]): Session Field (see EPC Gen2 Spec)
            target (Union[Unset, QueryTarget]): Target Field (see EPC Gen2 Spec)
     """

    tag_population: Union[Unset, int] = UNSET
    sel: Union[Unset, QuerySel] = UNSET
    session: Union[Unset, QuerySession] = UNSET
    target: Union[Unset, QueryTarget] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        tag_population = self.tag_population

        sel: Union[Unset, str] = UNSET
        if not isinstance(self.sel, Unset):
            sel = self.sel


        session: Union[Unset, str] = UNSET
        if not isinstance(self.session, Unset):
            session = self.session


        target: Union[Unset, str] = UNSET
        if not isinstance(self.target, Unset):
            target = self.target



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if tag_population is not UNSET:
            field_dict["tagPopulation"] = tag_population
        if sel is not UNSET:
            field_dict["sel"] = sel
        if session is not UNSET:
            field_dict["session"] = session
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tag_population = d.pop("tagPopulation", UNSET)

        _sel = d.pop("sel", UNSET)
        sel: Union[Unset, QuerySel]
        if isinstance(_sel,  Unset):
            sel = UNSET
        else:
            sel = check_query_sel(_sel)




        _session = d.pop("session", UNSET)
        session: Union[Unset, QuerySession]
        if isinstance(_session,  Unset):
            session = UNSET
        else:
            session = check_query_session(_session)




        _target = d.pop("target", UNSET)
        target: Union[Unset, QueryTarget]
        if isinstance(_target,  Unset):
            target = UNSET
        else:
            target = check_query_target(_target)




        query = cls(
            tag_population=tag_population,
            sel=sel,
            session=session,
            target=target,
        )


        query.additional_properties = d
        return query

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
