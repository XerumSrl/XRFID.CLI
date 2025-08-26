from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reader_stats_antennas_0 import check_reader_stats_antennas_0
from ..models.reader_stats_antennas_0 import ReaderStatsAntennas0
from ..models.reader_stats_antennas_1 import check_reader_stats_antennas_1
from ..models.reader_stats_antennas_1 import ReaderStatsAntennas1
from ..models.reader_stats_antennas_10 import check_reader_stats_antennas_10
from ..models.reader_stats_antennas_10 import ReaderStatsAntennas10
from ..models.reader_stats_antennas_11 import check_reader_stats_antennas_11
from ..models.reader_stats_antennas_11 import ReaderStatsAntennas11
from ..models.reader_stats_antennas_12 import check_reader_stats_antennas_12
from ..models.reader_stats_antennas_12 import ReaderStatsAntennas12
from ..models.reader_stats_antennas_13 import check_reader_stats_antennas_13
from ..models.reader_stats_antennas_13 import ReaderStatsAntennas13
from ..models.reader_stats_antennas_2 import check_reader_stats_antennas_2
from ..models.reader_stats_antennas_2 import ReaderStatsAntennas2
from ..models.reader_stats_antennas_3 import check_reader_stats_antennas_3
from ..models.reader_stats_antennas_3 import ReaderStatsAntennas3
from ..models.reader_stats_antennas_4 import check_reader_stats_antennas_4
from ..models.reader_stats_antennas_4 import ReaderStatsAntennas4
from ..models.reader_stats_antennas_5 import check_reader_stats_antennas_5
from ..models.reader_stats_antennas_5 import ReaderStatsAntennas5
from ..models.reader_stats_antennas_6 import check_reader_stats_antennas_6
from ..models.reader_stats_antennas_6 import ReaderStatsAntennas6
from ..models.reader_stats_antennas_7 import check_reader_stats_antennas_7
from ..models.reader_stats_antennas_7 import ReaderStatsAntennas7
from ..models.reader_stats_antennas_8 import check_reader_stats_antennas_8
from ..models.reader_stats_antennas_8 import ReaderStatsAntennas8
from ..models.reader_stats_antennas_9 import check_reader_stats_antennas_9
from ..models.reader_stats_antennas_9 import ReaderStatsAntennas9
from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="ReaderStatsAntennas")



@_attrs_define
class ReaderStatsAntennas:
    """ Status of the antennas connection

        Attributes:
            1 (ReaderStatsAntennas1): Antenna 1 connection state
            2 (ReaderStatsAntennas2): Antenna 2 connection state
            0 (Union[Unset, ReaderStatsAntennas0]): Antenna 0 connection state (only applicable to ATR7000)
            3 (Union[Unset, ReaderStatsAntennas3]): Antenna 3 connection state
            4 (Union[Unset, ReaderStatsAntennas4]): Antenna 4 connection state
            5 (Union[Unset, ReaderStatsAntennas5]): Antenna 5 connection state
            6 (Union[Unset, ReaderStatsAntennas6]): Antenna 6 connection state
            7 (Union[Unset, ReaderStatsAntennas7]): Antenna 7 connection state
            8 (Union[Unset, ReaderStatsAntennas8]): Antenna 8 connection state
            9 (Union[Unset, ReaderStatsAntennas9]): Antenna 9 connection state (only applicable to ATR7000)
            10 (Union[Unset, ReaderStatsAntennas10]): Antenna 10 connection state (only applicable to ATR7000)
            11 (Union[Unset, ReaderStatsAntennas11]): Antenna 11 connection state (only applicable to ATR7000)
            12 (Union[Unset, ReaderStatsAntennas12]): Antenna 12 connection state (only applicable to ATR7000)
            13 (Union[Unset, ReaderStatsAntennas13]): Antenna 13 connection state (only applicable to ATR7000)
     """

    1: ReaderStatsAntennas1
    2: ReaderStatsAntennas2
    0: Union[Unset, ReaderStatsAntennas0] = UNSET
    3: Union[Unset, ReaderStatsAntennas3] = UNSET
    4: Union[Unset, ReaderStatsAntennas4] = UNSET
    5: Union[Unset, ReaderStatsAntennas5] = UNSET
    6: Union[Unset, ReaderStatsAntennas6] = UNSET
    7: Union[Unset, ReaderStatsAntennas7] = UNSET
    8: Union[Unset, ReaderStatsAntennas8] = UNSET
    9: Union[Unset, ReaderStatsAntennas9] = UNSET
    10: Union[Unset, ReaderStatsAntennas10] = UNSET
    11: Union[Unset, ReaderStatsAntennas11] = UNSET
    12: Union[Unset, ReaderStatsAntennas12] = UNSET
    13: Union[Unset, ReaderStatsAntennas13] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        1: str = self.1

        2: str = self.2

        0: Union[Unset, str] = UNSET
        if not isinstance(self.0, Unset):
            0 = self.0


        3: Union[Unset, str] = UNSET
        if not isinstance(self.3, Unset):
            3 = self.3


        4: Union[Unset, str] = UNSET
        if not isinstance(self.4, Unset):
            4 = self.4


        5: Union[Unset, str] = UNSET
        if not isinstance(self.5, Unset):
            5 = self.5


        6: Union[Unset, str] = UNSET
        if not isinstance(self.6, Unset):
            6 = self.6


        7: Union[Unset, str] = UNSET
        if not isinstance(self.7, Unset):
            7 = self.7


        8: Union[Unset, str] = UNSET
        if not isinstance(self.8, Unset):
            8 = self.8


        9: Union[Unset, str] = UNSET
        if not isinstance(self.9, Unset):
            9 = self.9


        10: Union[Unset, str] = UNSET
        if not isinstance(self.10, Unset):
            10 = self.10


        11: Union[Unset, str] = UNSET
        if not isinstance(self.11, Unset):
            11 = self.11


        12: Union[Unset, str] = UNSET
        if not isinstance(self.12, Unset):
            12 = self.12


        13: Union[Unset, str] = UNSET
        if not isinstance(self.13, Unset):
            13 = self.13



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "1": 1,
            "2": 2,
        })
        if 0 is not UNSET:
            field_dict["0"] = 0
        if 3 is not UNSET:
            field_dict["3"] = 3
        if 4 is not UNSET:
            field_dict["4"] = 4
        if 5 is not UNSET:
            field_dict["5"] = 5
        if 6 is not UNSET:
            field_dict["6"] = 6
        if 7 is not UNSET:
            field_dict["7"] = 7
        if 8 is not UNSET:
            field_dict["8"] = 8
        if 9 is not UNSET:
            field_dict["9"] = 9
        if 10 is not UNSET:
            field_dict["10"] = 10
        if 11 is not UNSET:
            field_dict["11"] = 11
        if 12 is not UNSET:
            field_dict["12"] = 12
        if 13 is not UNSET:
            field_dict["13"] = 13

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        1 = check_reader_stats_antennas_1(d.pop("1"))




        2 = check_reader_stats_antennas_2(d.pop("2"))




        _0 = d.pop("0", UNSET)
        0: Union[Unset, ReaderStatsAntennas0]
        if isinstance(_0,  Unset):
            0 = UNSET
        else:
            0 = check_reader_stats_antennas_0(_0)




        _3 = d.pop("3", UNSET)
        3: Union[Unset, ReaderStatsAntennas3]
        if isinstance(_3,  Unset):
            3 = UNSET
        else:
            3 = check_reader_stats_antennas_3(_3)




        _4 = d.pop("4", UNSET)
        4: Union[Unset, ReaderStatsAntennas4]
        if isinstance(_4,  Unset):
            4 = UNSET
        else:
            4 = check_reader_stats_antennas_4(_4)




        _5 = d.pop("5", UNSET)
        5: Union[Unset, ReaderStatsAntennas5]
        if isinstance(_5,  Unset):
            5 = UNSET
        else:
            5 = check_reader_stats_antennas_5(_5)




        _6 = d.pop("6", UNSET)
        6: Union[Unset, ReaderStatsAntennas6]
        if isinstance(_6,  Unset):
            6 = UNSET
        else:
            6 = check_reader_stats_antennas_6(_6)




        _7 = d.pop("7", UNSET)
        7: Union[Unset, ReaderStatsAntennas7]
        if isinstance(_7,  Unset):
            7 = UNSET
        else:
            7 = check_reader_stats_antennas_7(_7)




        _8 = d.pop("8", UNSET)
        8: Union[Unset, ReaderStatsAntennas8]
        if isinstance(_8,  Unset):
            8 = UNSET
        else:
            8 = check_reader_stats_antennas_8(_8)




        _9 = d.pop("9", UNSET)
        9: Union[Unset, ReaderStatsAntennas9]
        if isinstance(_9,  Unset):
            9 = UNSET
        else:
            9 = check_reader_stats_antennas_9(_9)




        _10 = d.pop("10", UNSET)
        10: Union[Unset, ReaderStatsAntennas10]
        if isinstance(_10,  Unset):
            10 = UNSET
        else:
            10 = check_reader_stats_antennas_10(_10)




        _11 = d.pop("11", UNSET)
        11: Union[Unset, ReaderStatsAntennas11]
        if isinstance(_11,  Unset):
            11 = UNSET
        else:
            11 = check_reader_stats_antennas_11(_11)




        _12 = d.pop("12", UNSET)
        12: Union[Unset, ReaderStatsAntennas12]
        if isinstance(_12,  Unset):
            12 = UNSET
        else:
            12 = check_reader_stats_antennas_12(_12)




        _13 = d.pop("13", UNSET)
        13: Union[Unset, ReaderStatsAntennas13]
        if isinstance(_13,  Unset):
            13 = UNSET
        else:
            13 = check_reader_stats_antennas_13(_13)




        reader_stats_antennas = cls(
            1=1,
            2=2,
            0=0,
            3=3,
            4=4,
            5=5,
            6=6,
            7=7,
            8=8,
            9=9,
            10=10,
            11=11,
            12=12,
            13=13,
        )


        reader_stats_antennas.additional_properties = d
        return reader_stats_antennas

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
