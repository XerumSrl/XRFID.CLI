from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.operating_mode_environment import check_operating_mode_environment
from ..models.operating_mode_environment import OperatingModeEnvironment
from ..models.operating_mode_type import check_operating_mode_type
from ..models.operating_mode_type import OperatingModeType
from ..models.tag_meta_data_v1_item import check_tag_meta_data_v1_item
from ..models.tag_meta_data_v1_item import TagMetaDataV1Item
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.delay_between_antenna_cycles import DelayBetweenAntennaCycles
  from ..models.antenna_stop_condition import AntennaStopCondition
  from ..models.portal_settings import PortalSettings
  from ..models.tag_id_filter import TagIdFilter
  from ..models.write import Write
  from ..models.lock import Lock
  from ..models.rssi_filter import RssiFilter
  from ..models.access import Access
  from ..models.read import Read
  from ..models.directionality_settings import DirectionalitySettings
  from ..models.query import Query
  from ..models.kill import Kill
  from ..models.report_filter import ReportFilter
  from ..models.radio_stop_conditions import RadioStopConditions
  from ..models.operating_mode_beams_item import OperatingModeBeamsItem
  from ..models.inventory_settings import InventorySettings
  from ..models.radio_start_conditions import RadioStartConditions





T = TypeVar("T", bound="OperatingMode")



@_attrs_define
class OperatingMode:
    """ Represents the reader operating mode.

        Example:
            {'type': 'INVENTORY', 'antennas': [1, 2, 3], 'transmitPower': 30.1, 'antennaStopCondition': [{'type':
                'DURATION', 'value': 500}, {'type': 'INVENTORY_COUNT', 'value': 1}, {'type': 'GPI', 'value': {'port': 2,
                'signal': 'HIGH'}}], 'tagMetaData': ['PC', 'CRC', {'userDefined': 'readerABC'}], 'rssiFilter': {'threshold':
                -72}}

        Attributes:
            type_ (OperatingModeType): The type of mode of operation  Default: 'SIMPLE'.
            mode_specific_settings (Union['DirectionalitySettings', 'InventorySettings', 'PortalSettings', Unset]):
            environment (Union[Unset, OperatingModeEnvironment]):






































                  The type of environment in which the reader operates. Along with the regulatory configuration of the reader,
                the environment parameter will set the default link profile parameters (i.e., Miller mode, BLF, Tari, etc.) and
                the receiver dynamic range (interference immunity).

                  LOW_INTERFERENCE:  The reader is operating in an environment when the likelihood of interference is very low
                or only occurs for very brief periods of time (defined as a single interrogator environment in the Gen2 and ISO
                standards).

                  HIGH_INTERFERENCE: The reader is operating in the presence of other readers (defined as a multi-interrogator
                or dense interrogator environment in the Gen2 and ISO standards).

                  VERY_HIGH_INTERFERENCE: The reader is operating in an environment where the number of readers is greater than
                the number of available channels, or when interfering readers are in very close proximity to each other.

                  AUTO_DETECT: This will cause the reader to try and assess the environment and adjust accordingly.

                  DEMO: Should be used when demonstrating the maximum performance (fastest read rate) of a reader. This assumes
                no other readers in the environement.

                  If absent, the environment is set to HIGH_INTERFERENCE Default: 'HIGH_INTERFERENCE'.
            antennas (Union[Unset, list[int]]):






































                 An array of integers representing the antenna ports to use to read tags. For ATR, the integers represent beam
                numbers.

                 If absent, all antennas ports are used; for the ATR, a set of 38 beams are used.
            filter_ (Union[Unset, TagIdFilter]): Represents filter on the tag id.

                If absent, no filter is used.
            transmit_power (Union[Unset, float, list[float]]): Desired Transmit Power (in dbm).
                If absent, the value is set to 27 dbm; for the ATR, the value is set to 36 dbm EIRP.
            antenna_stop_condition (Union['AntennaStopCondition', Unset, list['AntennaStopCondition']]): Stop Condition for
                antennas.
                If absent, the antenna stop condition is set to run a single inventory round for no longer than 1/N seconds.
                Where N is the number of enabled antennas.
            query (Union['Query', Unset, list['Query']]): Gen2 query parameters. See Gen2 spec for details.
                If absent, "sel" is set to ALL, session is set to 1, target is set to A, and tag population set to 1.
            selects (Union[Any, Unset]): Gen2 select parameters. See Gen2 spec for details.
                If absent, no select will be issued. Cannot be set when filter with prefix type is also set.
                If there is an array of select objects, all of the selects in the array will be applied to all antennas.
                If there is an array of array of select objects, each array of select objects will apply to each antenna. The
                array of arrays must have the same number of entries as the antennas array.
            delay_after_selects (Union[Unset, int]): Duration in milliseconds to wait after issuing the final select before
                issuing a query. If absent, the minimum time will be used.
            accesses (Union[Unset, list[Union['Access', 'Kill', 'Lock', 'Read', 'Write']], list[list[Union['Access', 'Kill',
                'Lock', 'Read', 'Write']]]]):






































                 Gen2 access parameters. See Gen2 spec for details.

                 If absent, no access will be issued.

                 If there is an array of access objects, all of the accesss in the array will be applied to all antennas.

                 If there is an array of array of access objects, each array of access objects will apply to each antenna. The
                array of arrays must have the same number of entries as the antennas array.
            delay_between_antenna_cycles (Union[Unset, DelayBetweenAntennaCycles]): This introduces a delay between antenna
                cycles if no tags are read or if no unique tags are read. This allows the reader to share the spectrum if there
                are no tags to be read.

                If absent,
                on the ATR7000 and the FX9600, delayBetweenAntennas cycles is set to wait for 75 mS if no unique tags are read
                during a antenna cycle.
                on the FX7500, delayBetweenAntennas cycles is set to wait for 75 mS if no tags are read during a antenna cycle.
            tag_meta_data (Union[Unset, list[TagMetaDataV1Item]]): Controls the metadata that is sent when a tag is reported

                  “ANTENNA” will report the antenna port upon which the tag was inventoried.

                  “RSSI” will report the rssi (in dbm) of the inventoried tag. If the tag is only reported occasionally (see
                reportFilter), this tag will be the peak rssi since the last reported read.

                   “PHASE” will report the phase (in degrees) of the inventoried tag. This value will only be reported if each
                individual tag read is reported (in other words, if reportFilter duration is set to 0). Otherwise, it will not
                be reported.

                  “CHANNEL” will report the channel (in MHz) the reader was using when the tag was inventoried. This value will
                only be reported if each individual tag read is reported (in other words, if reportFilter duration is set to 0).
                Otherwise, it will not be reported.

                  “SEEN_COUNT” will report the number of times the tag has been inventoried since the previous report. This
                value will always be 1 if each individual tag read is reported (in other words, if reportFilter duration is set
                to 0).

                  “PC” will report the PC bits of the inventoried tag as a hex string.

                  “XPC” will report the XPC bits of the inventoried tag, if present, as a hex string.

                  “CRC” will report the CRC bits of the inventoried tag as a hex string.

                  “EPC” will report the entire contents of the EPC bank as a hex string. If only a portion of the memory bank is
                desired, this can be requested by appending a [] to the string and placing the words requested. For instance, if
                only the first word is desired, the value can be set as “EPC[1]”. If the first word and the 3-5 word are
                desired, the value can be set to “EPC[1,3-5]”.

                  “TID” will report the entire contents of the TID bank as a hex string. If only a portion of the memory bank is
                desired, this can be requested by appending a [] to the string and placing the words requested. For instance, if
                only the first word is desired, the value can be set as “TID[1]”. If the first word and the 3-5 word are
                desired, the value can be set to “TID[1,3-5]”.

                  “USER” will report the entire contents of the USER bank as a hex string. If only a portion of the memory bank
                is desired, this can be requested by appending a [] to the string and placing the words requested. For instance,
                if only the first word is desired, the value can be set as “TID[1]”. If the first word and the 3-5 word are
                desired, the value can be set to “TID[1,3-5]”.

                  “MAC” will report the MAC Address of the reader reporting the tag.

                  “HOSTNAME” will report the hostname of the reader reporting the tag.

                  “TAGURI” will report the GS1 TDS decoded “EPC Tag URI”. See GS1 TDS documentation for details.

                  “EPCURI” will report the GS1 TDS decoded “Pure Identity EPC URI”. See GS1 TDS documentation for details.

                The array may also contain an object or objects. The object must contain a single name value pair with the name
                being set to “userDefined” or “antennaNames”


                If absent,
                “SIMPLE” mode does not report any additional meta data, “PORTAL” and “CONVEYOR” modes reports “ANTENNA”, and
                “INVENTORY” mode reports “ANTENNA”, “RSSI”, and “SEEN_COUNT”.
            radio_start_conditions (Union[Unset, RadioStartConditions]): Controls when, after a “start” is issued, the radio
                starts trying to inventory tags.

                If absent, the radio will immediately begin inventorying tags upon a "start" command.
            radio_stop_conditions (Union[Unset, RadioStopConditions]): Controls when an ongoing operation completes.

                If absent, the radio will continue trying to inventory tags until a "stop" is issued.
            report_filter (Union[Unset, ReportFilter]): Controls when and how often a tag is reported

                NOTE: This cannot be set while in "INVENTORY" mode. Setting the modeSpecificSetting for interval must be used in
                "INVENTORY" mode.

                If absent, each mode uses a different default.

                "SIMPLE": report tag read once.

                "PORTAL" and "CONVEYOR": report each tag the first time it is read on each antenna.
            rssi_filter (Union[Unset, RssiFilter]): Tag with RSSI below threshold will not be inventoried by the radio

                If absent, rssi filter is not used.

                Note: Currently ONLY supported by the FX9600.
            beams (Union[Unset, list['OperatingModeBeamsItem']]): Array of beams to use

                Note : beams is only supported for ATR7000 reader
     """

    type_: OperatingModeType = 'SIMPLE'
    mode_specific_settings: Union['DirectionalitySettings', 'InventorySettings', 'PortalSettings', Unset] = UNSET
    environment: Union[Unset, OperatingModeEnvironment] = 'HIGH_INTERFERENCE'
    antennas: Union[Unset, list[int]] = UNSET
    filter_: Union[Unset, 'TagIdFilter'] = UNSET
    transmit_power: Union[Unset, float, list[float]] = UNSET
    antenna_stop_condition: Union['AntennaStopCondition', Unset, list['AntennaStopCondition']] = UNSET
    query: Union['Query', Unset, list['Query']] = UNSET
    selects: Union[Any, Unset] = UNSET
    delay_after_selects: Union[Unset, int] = UNSET
    accesses: Union[Unset, list[Union['Access', 'Kill', 'Lock', 'Read', 'Write']], list[list[Union['Access', 'Kill', 'Lock', 'Read', 'Write']]]] = UNSET
    delay_between_antenna_cycles: Union[Unset, 'DelayBetweenAntennaCycles'] = UNSET
    tag_meta_data: Union[Unset, list[TagMetaDataV1Item]] = UNSET
    radio_start_conditions: Union[Unset, 'RadioStartConditions'] = UNSET
    radio_stop_conditions: Union[Unset, 'RadioStopConditions'] = UNSET
    report_filter: Union[Unset, 'ReportFilter'] = UNSET
    rssi_filter: Union[Unset, 'RssiFilter'] = UNSET
    beams: Union[Unset, list['OperatingModeBeamsItem']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.delay_between_antenna_cycles import DelayBetweenAntennaCycles
        from ..models.antenna_stop_condition import AntennaStopCondition
        from ..models.portal_settings import PortalSettings
        from ..models.tag_id_filter import TagIdFilter
        from ..models.write import Write
        from ..models.lock import Lock
        from ..models.rssi_filter import RssiFilter
        from ..models.access import Access
        from ..models.read import Read
        from ..models.directionality_settings import DirectionalitySettings
        from ..models.query import Query
        from ..models.kill import Kill
        from ..models.report_filter import ReportFilter
        from ..models.radio_stop_conditions import RadioStopConditions
        from ..models.operating_mode_beams_item import OperatingModeBeamsItem
        from ..models.inventory_settings import InventorySettings
        from ..models.radio_start_conditions import RadioStartConditions
        type_: str = self.type_

        mode_specific_settings: Union[Unset, dict[str, Any]]
        if isinstance(self.mode_specific_settings, Unset):
            mode_specific_settings = UNSET
        elif isinstance(self.mode_specific_settings, InventorySettings):
            mode_specific_settings = self.mode_specific_settings.to_dict()
        elif isinstance(self.mode_specific_settings, PortalSettings):
            mode_specific_settings = self.mode_specific_settings.to_dict()
        else:
            mode_specific_settings = self.mode_specific_settings.to_dict()


        environment: Union[Unset, str] = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment


        antennas: Union[Unset, list[int]] = UNSET
        if not isinstance(self.antennas, Unset):
            antennas = self.antennas



        filter_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        transmit_power: Union[Unset, float, list[float]]
        if isinstance(self.transmit_power, Unset):
            transmit_power = UNSET
        elif isinstance(self.transmit_power, list):
            transmit_power = self.transmit_power


        else:
            transmit_power = self.transmit_power

        antenna_stop_condition: Union[Unset, dict[str, Any], list[dict[str, Any]]]
        if isinstance(self.antenna_stop_condition, Unset):
            antenna_stop_condition = UNSET
        elif isinstance(self.antenna_stop_condition, AntennaStopCondition):
            antenna_stop_condition = self.antenna_stop_condition.to_dict()
        else:
            antenna_stop_condition = []
            for antenna_stop_condition_type_1_item_data in self.antenna_stop_condition:
                antenna_stop_condition_type_1_item = antenna_stop_condition_type_1_item_data.to_dict()
                antenna_stop_condition.append(antenna_stop_condition_type_1_item)




        query: Union[Unset, dict[str, Any], list[dict[str, Any]]]
        if isinstance(self.query, Unset):
            query = UNSET
        elif isinstance(self.query, Query):
            query = self.query.to_dict()
        else:
            query = []
            for query_type_1_item_data in self.query:
                query_type_1_item = query_type_1_item_data.to_dict()
                query.append(query_type_1_item)




        selects: Union[Any, Unset]
        if isinstance(self.selects, Unset):
            selects = UNSET
        else:
            selects = self.selects

        delay_after_selects = self.delay_after_selects

        accesses: Union[Unset, list[dict[str, Any]], list[list[dict[str, Any]]]]
        if isinstance(self.accesses, Unset):
            accesses = UNSET
        elif isinstance(self.accesses, list):
            accesses = []
            for componentsschemasaccess_cmds_v1_item_data in self.accesses:
                componentsschemasaccess_cmds_v1_item: dict[str, Any]
                if isinstance(componentsschemasaccess_cmds_v1_item_data, Read):
                    componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                elif isinstance(componentsschemasaccess_cmds_v1_item_data, Write):
                    componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                elif isinstance(componentsschemasaccess_cmds_v1_item_data, Access):
                    componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                elif isinstance(componentsschemasaccess_cmds_v1_item_data, Lock):
                    componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                else:
                    componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()

                accesses.append(componentsschemasaccess_cmds_v1_item)


        else:
            accesses = []
            for accesses_type_1_item_data in self.accesses:
                accesses_type_1_item = []
                for componentsschemasaccess_cmds_v1_item_data in accesses_type_1_item_data:
                    componentsschemasaccess_cmds_v1_item: dict[str, Any]
                    if isinstance(componentsschemasaccess_cmds_v1_item_data, Read):
                        componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                    elif isinstance(componentsschemasaccess_cmds_v1_item_data, Write):
                        componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                    elif isinstance(componentsschemasaccess_cmds_v1_item_data, Access):
                        componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                    elif isinstance(componentsschemasaccess_cmds_v1_item_data, Lock):
                        componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()
                    else:
                        componentsschemasaccess_cmds_v1_item = componentsschemasaccess_cmds_v1_item_data.to_dict()

                    accesses_type_1_item.append(componentsschemasaccess_cmds_v1_item)


                accesses.append(accesses_type_1_item)




        delay_between_antenna_cycles: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.delay_between_antenna_cycles, Unset):
            delay_between_antenna_cycles = self.delay_between_antenna_cycles.to_dict()

        tag_meta_data: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tag_meta_data, Unset):
            tag_meta_data = []
            for componentsschemastag_meta_data_v_1_item_data in self.tag_meta_data:
                componentsschemastag_meta_data_v_1_item: str = componentsschemastag_meta_data_v_1_item_data
                tag_meta_data.append(componentsschemastag_meta_data_v_1_item)



        radio_start_conditions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.radio_start_conditions, Unset):
            radio_start_conditions = self.radio_start_conditions.to_dict()

        radio_stop_conditions: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.radio_stop_conditions, Unset):
            radio_stop_conditions = self.radio_stop_conditions.to_dict()

        report_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.report_filter, Unset):
            report_filter = self.report_filter.to_dict()

        rssi_filter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rssi_filter, Unset):
            rssi_filter = self.rssi_filter.to_dict()

        beams: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.beams, Unset):
            beams = []
            for beams_item_data in self.beams:
                beams_item = beams_item_data.to_dict()
                beams.append(beams_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if mode_specific_settings is not UNSET:
            field_dict["modeSpecificSettings"] = mode_specific_settings
        if environment is not UNSET:
            field_dict["environment"] = environment
        if antennas is not UNSET:
            field_dict["antennas"] = antennas
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if transmit_power is not UNSET:
            field_dict["transmitPower"] = transmit_power
        if antenna_stop_condition is not UNSET:
            field_dict["antennaStopCondition"] = antenna_stop_condition
        if query is not UNSET:
            field_dict["query"] = query
        if selects is not UNSET:
            field_dict["selects"] = selects
        if delay_after_selects is not UNSET:
            field_dict["delayAfterSelects"] = delay_after_selects
        if accesses is not UNSET:
            field_dict["accesses"] = accesses
        if delay_between_antenna_cycles is not UNSET:
            field_dict["delayBetweenAntennaCycles"] = delay_between_antenna_cycles
        if tag_meta_data is not UNSET:
            field_dict["tagMetaData"] = tag_meta_data
        if radio_start_conditions is not UNSET:
            field_dict["radioStartConditions"] = radio_start_conditions
        if radio_stop_conditions is not UNSET:
            field_dict["radioStopConditions"] = radio_stop_conditions
        if report_filter is not UNSET:
            field_dict["reportFilter"] = report_filter
        if rssi_filter is not UNSET:
            field_dict["rssiFilter"] = rssi_filter
        if beams is not UNSET:
            field_dict["beams"] = beams

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delay_between_antenna_cycles import DelayBetweenAntennaCycles
        from ..models.antenna_stop_condition import AntennaStopCondition
        from ..models.portal_settings import PortalSettings
        from ..models.tag_id_filter import TagIdFilter
        from ..models.write import Write
        from ..models.lock import Lock
        from ..models.rssi_filter import RssiFilter
        from ..models.access import Access
        from ..models.read import Read
        from ..models.directionality_settings import DirectionalitySettings
        from ..models.query import Query
        from ..models.kill import Kill
        from ..models.report_filter import ReportFilter
        from ..models.radio_stop_conditions import RadioStopConditions
        from ..models.operating_mode_beams_item import OperatingModeBeamsItem
        from ..models.inventory_settings import InventorySettings
        from ..models.radio_start_conditions import RadioStartConditions
        d = dict(src_dict)
        type_ = check_operating_mode_type(d.pop("type"))




        def _parse_mode_specific_settings(data: object) -> Union['DirectionalitySettings', 'InventorySettings', 'PortalSettings', Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mode_specific_settings_type_0 = InventorySettings.from_dict(data)



                return mode_specific_settings_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mode_specific_settings_type_1 = PortalSettings.from_dict(data)



                return mode_specific_settings_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            mode_specific_settings_type_2 = DirectionalitySettings.from_dict(data)



            return mode_specific_settings_type_2

        mode_specific_settings = _parse_mode_specific_settings(d.pop("modeSpecificSettings", UNSET))


        _environment = d.pop("environment", UNSET)
        environment: Union[Unset, OperatingModeEnvironment]
        if isinstance(_environment,  Unset):
            environment = UNSET
        else:
            environment = check_operating_mode_environment(_environment)




        antennas = cast(list[int], d.pop("antennas", UNSET))


        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, TagIdFilter]
        if isinstance(_filter_,  Unset):
            filter_ = UNSET
        else:
            filter_ = TagIdFilter.from_dict(_filter_)




        def _parse_transmit_power(data: object) -> Union[Unset, float, list[float]]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                transmit_power_type_1 = cast(list[float], data)

                return transmit_power_type_1
            except: # noqa: E722
                pass
            return cast(Union[Unset, float, list[float]], data)

        transmit_power = _parse_transmit_power(d.pop("transmitPower", UNSET))


        def _parse_antenna_stop_condition(data: object) -> Union['AntennaStopCondition', Unset, list['AntennaStopCondition']]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                antenna_stop_condition_type_0 = AntennaStopCondition.from_dict(data)



                return antenna_stop_condition_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            antenna_stop_condition_type_1 = []
            _antenna_stop_condition_type_1 = data
            for antenna_stop_condition_type_1_item_data in (_antenna_stop_condition_type_1):
                antenna_stop_condition_type_1_item = AntennaStopCondition.from_dict(antenna_stop_condition_type_1_item_data)



                antenna_stop_condition_type_1.append(antenna_stop_condition_type_1_item)

            return antenna_stop_condition_type_1

        antenna_stop_condition = _parse_antenna_stop_condition(d.pop("antennaStopCondition", UNSET))


        def _parse_query(data: object) -> Union['Query', Unset, list['Query']]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                query_type_0 = Query.from_dict(data)



                return query_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            query_type_1 = []
            _query_type_1 = data
            for query_type_1_item_data in (_query_type_1):
                query_type_1_item = Query.from_dict(query_type_1_item_data)



                query_type_1.append(query_type_1_item)

            return query_type_1

        query = _parse_query(d.pop("query", UNSET))


        def _parse_selects(data: object) -> Union[Any, Unset]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset], data)

        selects = _parse_selects(d.pop("selects", UNSET))


        delay_after_selects = d.pop("delayAfterSelects", UNSET)

        def _parse_accesses(data: object) -> Union[Unset, list[Union['Access', 'Kill', 'Lock', 'Read', 'Write']], list[list[Union['Access', 'Kill', 'Lock', 'Read', 'Write']]]]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                accesses_type_0 = []
                _accesses_type_0 = data
                for componentsschemasaccess_cmds_v1_item_data in (_accesses_type_0):
                    def _parse_componentsschemasaccess_cmds_v1_item(data: object) -> Union['Access', 'Kill', 'Lock', 'Read', 'Write']:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_0 = Read.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_0
                        except: # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_1 = Write.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_1
                        except: # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_2 = Access.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_2
                        except: # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_3 = Lock.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_3
                        except: # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemasaccess_cmds_v1_item_type_4 = Kill.from_dict(data)



                        return componentsschemasaccess_cmds_v1_item_type_4

                    componentsschemasaccess_cmds_v1_item = _parse_componentsschemasaccess_cmds_v1_item(componentsschemasaccess_cmds_v1_item_data)

                    accesses_type_0.append(componentsschemasaccess_cmds_v1_item)

                return accesses_type_0
            except: # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            accesses_type_1 = []
            _accesses_type_1 = data
            for accesses_type_1_item_data in (_accesses_type_1):
                accesses_type_1_item = []
                _accesses_type_1_item = accesses_type_1_item_data
                for componentsschemasaccess_cmds_v1_item_data in (_accesses_type_1_item):
                    def _parse_componentsschemasaccess_cmds_v1_item(data: object) -> Union['Access', 'Kill', 'Lock', 'Read', 'Write']:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_0 = Read.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_0
                        except: # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_1 = Write.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_1
                        except: # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_2 = Access.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_2
                        except: # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            componentsschemasaccess_cmds_v1_item_type_3 = Lock.from_dict(data)



                            return componentsschemasaccess_cmds_v1_item_type_3
                        except: # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        componentsschemasaccess_cmds_v1_item_type_4 = Kill.from_dict(data)



                        return componentsschemasaccess_cmds_v1_item_type_4

                    componentsschemasaccess_cmds_v1_item = _parse_componentsschemasaccess_cmds_v1_item(componentsschemasaccess_cmds_v1_item_data)

                    accesses_type_1_item.append(componentsschemasaccess_cmds_v1_item)

                accesses_type_1.append(accesses_type_1_item)

            return accesses_type_1

        accesses = _parse_accesses(d.pop("accesses", UNSET))


        _delay_between_antenna_cycles = d.pop("delayBetweenAntennaCycles", UNSET)
        delay_between_antenna_cycles: Union[Unset, DelayBetweenAntennaCycles]
        if isinstance(_delay_between_antenna_cycles,  Unset):
            delay_between_antenna_cycles = UNSET
        else:
            delay_between_antenna_cycles = DelayBetweenAntennaCycles.from_dict(_delay_between_antenna_cycles)




        tag_meta_data = []
        _tag_meta_data = d.pop("tagMetaData", UNSET)
        for componentsschemastag_meta_data_v_1_item_data in (_tag_meta_data or []):
            componentsschemastag_meta_data_v_1_item = check_tag_meta_data_v1_item(componentsschemastag_meta_data_v_1_item_data)



            tag_meta_data.append(componentsschemastag_meta_data_v_1_item)


        _radio_start_conditions = d.pop("radioStartConditions", UNSET)
        radio_start_conditions: Union[Unset, RadioStartConditions]
        if isinstance(_radio_start_conditions,  Unset):
            radio_start_conditions = UNSET
        else:
            radio_start_conditions = RadioStartConditions.from_dict(_radio_start_conditions)




        _radio_stop_conditions = d.pop("radioStopConditions", UNSET)
        radio_stop_conditions: Union[Unset, RadioStopConditions]
        if isinstance(_radio_stop_conditions,  Unset):
            radio_stop_conditions = UNSET
        else:
            radio_stop_conditions = RadioStopConditions.from_dict(_radio_stop_conditions)




        _report_filter = d.pop("reportFilter", UNSET)
        report_filter: Union[Unset, ReportFilter]
        if isinstance(_report_filter,  Unset):
            report_filter = UNSET
        else:
            report_filter = ReportFilter.from_dict(_report_filter)




        _rssi_filter = d.pop("rssiFilter", UNSET)
        rssi_filter: Union[Unset, RssiFilter]
        if isinstance(_rssi_filter,  Unset):
            rssi_filter = UNSET
        else:
            rssi_filter = RssiFilter.from_dict(_rssi_filter)




        beams = []
        _beams = d.pop("beams", UNSET)
        for beams_item_data in (_beams or []):
            beams_item = OperatingModeBeamsItem.from_dict(beams_item_data)



            beams.append(beams_item)


        operating_mode = cls(
            type_=type_,
            mode_specific_settings=mode_specific_settings,
            environment=environment,
            antennas=antennas,
            filter_=filter_,
            transmit_power=transmit_power,
            antenna_stop_condition=antenna_stop_condition,
            query=query,
            selects=selects,
            delay_after_selects=delay_after_selects,
            accesses=accesses,
            delay_between_antenna_cycles=delay_between_antenna_cycles,
            tag_meta_data=tag_meta_data,
            radio_start_conditions=radio_start_conditions,
            radio_stop_conditions=radio_stop_conditions,
            report_filter=report_filter,
            rssi_filter=rssi_filter,
            beams=beams,
        )


        operating_mode.additional_properties = d
        return operating_mode

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
