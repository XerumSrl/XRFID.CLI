from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.directionality_settings_advanced_config_debug_level import check_directionality_settings_advanced_config_debug_level
from ..models.directionality_settings_advanced_config_debug_level import DirectionalitySettingsAdvancedConfigDebugLevel
from ..models.directionality_settings_advanced_config_report_direction_item import check_directionality_settings_advanced_config_report_direction_item
from ..models.directionality_settings_advanced_config_report_direction_item import DirectionalitySettingsAdvancedConfigReportDirectionItem
from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union

if TYPE_CHECKING:
  from ..models.directionality_settings_advanced_config_user_defined_type_1 import DirectionalitySettingsAdvancedConfigUserDefinedType1





T = TypeVar("T", bound="DirectionalitySettingsAdvancedConfig")



@_attrs_define
class DirectionalitySettingsAdvancedConfig:
    """ Advanced Directionality Configuration

        Attributes:
            report_new (Union[Unset, bool]): Report (or do not report) "NEW" events Default: True.
            report_transition (Union[Unset, bool]): Report (or do not report) "TRANSITION" events Default: True.
            report_timed_out (Union[Unset, bool]): Report (or do not report) "TIMED_OUT" events Default: True.
            report_direction (Union[Unset, list[DirectionalitySettingsAdvancedConfigReportDirectionItem]]): Direction events
                to report in "TIMED_OUT" event. If "TIMED_OUT" event is enabled only report "TIMED_OUT" if one of the direction
                events in this list.
            report_location_history (Union[Unset, bool]): Report (or do not report) location history in "TIMED_OUT" event
                Default: False.
            report_zone_history (Union[Unset, bool]): Report (or do not report) zone history in "TIMED_OUT" event Default:
                False.
            report_update_duration_seconds (Union[Unset, float]): Duration to report tag updates even if no transition
                (value in seconds) (-1 is never report) Default: -1.0.
            report_raw (Union[Unset, bool]): Report (or do not report) raw bearing/location messages Default: False.
            tag_timeout_seconds_min (Union[Unset, float]): Minimum duration until a tag is deemed "gone" (in seconds)
                Default: 30.0.
            tag_timeout_seconds_default (Union[Unset, float]): Default duration until a tag is deemed "gone" (in seconds)
                Default: 30.0.
            tag_timeout_seconds_max (Union[Unset, float]): Maximum duration until a tag is deemed "gone" (in seconds)
                Default: 3600.0.
            sigma_multiplier (Union[Unset, int]): Multiple of standard deviation of time between reads to determine adaptive
                timeout. Default: 5.
            background_processing_interval_seconds (Union[Unset, float]): Interval between processing incoming raw messages
                (in seconds) Default: 0.5.
            direction_lookback_seconds (Union[Unset, float]): Duration (in seconds) prior to final tag read before timeout
                to consider for determining direction. Default: 5.0.
            ma_duration_seconds (Union[Unset, float]): Moving Average Window Duration (in seconds). Must be less than
                tag_timeout_seconds Default: 3.0.
            debug_level (Union[Unset, DirectionalitySettingsAdvancedConfigDebugLevel]): Set the debug logging level
                Default: 'INFO'.
            hysteresis_feet (Union[Unset, float]): Set the distance (in feet) a tag must travel into a zone to be able to
                move back into previous zone Default: 2.0.
            user_defined (Union['DirectionalitySettingsAdvancedConfigUserDefinedType1', Unset, str]): user defined value
                (string or object) that will be included in each directionality event
            regression_min_n (Union[Unset, int]): Minimum number of data points required by regression to give non-Unknown
                Direction Default: 3.
            regression_min_duration_seconds (Union[Unset, float]): Minimum duration (in seconds) of samples required within
                lookback window by regression to give non-Unknown Direction. The value should always be less than
                direction_lookback_seconds. Default: 0.75.
            regression_extrapolation_multiplier (Union[Unset, float]): Value used by regression to determine how far to
                extrapolate crossing outside of lookback duration Default: 1.0.
            regression_slope_threshold (Union[Unset, float]): Value of slope used by regression to distinguish between In
                and Out (and None) Direction Default: 0.0.
            confirm_direction_with_final_zone (Union[Unset, bool]): Boolean to treat direction as "unknown" if final zone
                conflicts with direction determined in regression Default: False.
            max_tags_limit (Union[Unset, int]): Number of tags to keep in application memory Default: 2000.
            raw_location_conf_threshold (Union[Unset, int]): Minimum value of the confidence of a raw location estimate to
                be used in location/zone/direction deteremination Default: 50.
     """

    report_new: Union[Unset, bool] = True
    report_transition: Union[Unset, bool] = True
    report_timed_out: Union[Unset, bool] = True
    report_direction: Union[Unset, list[DirectionalitySettingsAdvancedConfigReportDirectionItem]] = UNSET
    report_location_history: Union[Unset, bool] = False
    report_zone_history: Union[Unset, bool] = False
    report_update_duration_seconds: Union[Unset, float] = -1.0
    report_raw: Union[Unset, bool] = False
    tag_timeout_seconds_min: Union[Unset, float] = 30.0
    tag_timeout_seconds_default: Union[Unset, float] = 30.0
    tag_timeout_seconds_max: Union[Unset, float] = 3600.0
    sigma_multiplier: Union[Unset, int] = 5
    background_processing_interval_seconds: Union[Unset, float] = 0.5
    direction_lookback_seconds: Union[Unset, float] = 5.0
    ma_duration_seconds: Union[Unset, float] = 3.0
    debug_level: Union[Unset, DirectionalitySettingsAdvancedConfigDebugLevel] = 'INFO'
    hysteresis_feet: Union[Unset, float] = 2.0
    user_defined: Union['DirectionalitySettingsAdvancedConfigUserDefinedType1', Unset, str] = UNSET
    regression_min_n: Union[Unset, int] = 3
    regression_min_duration_seconds: Union[Unset, float] = 0.75
    regression_extrapolation_multiplier: Union[Unset, float] = 1.0
    regression_slope_threshold: Union[Unset, float] = 0.0
    confirm_direction_with_final_zone: Union[Unset, bool] = False
    max_tags_limit: Union[Unset, int] = 2000
    raw_location_conf_threshold: Union[Unset, int] = 50
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.directionality_settings_advanced_config_user_defined_type_1 import DirectionalitySettingsAdvancedConfigUserDefinedType1
        report_new = self.report_new

        report_transition = self.report_transition

        report_timed_out = self.report_timed_out

        report_direction: Union[Unset, list[str]] = UNSET
        if not isinstance(self.report_direction, Unset):
            report_direction = []
            for report_direction_item_data in self.report_direction:
                report_direction_item: str = report_direction_item_data
                report_direction.append(report_direction_item)



        report_location_history = self.report_location_history

        report_zone_history = self.report_zone_history

        report_update_duration_seconds = self.report_update_duration_seconds

        report_raw = self.report_raw

        tag_timeout_seconds_min = self.tag_timeout_seconds_min

        tag_timeout_seconds_default = self.tag_timeout_seconds_default

        tag_timeout_seconds_max = self.tag_timeout_seconds_max

        sigma_multiplier = self.sigma_multiplier

        background_processing_interval_seconds = self.background_processing_interval_seconds

        direction_lookback_seconds = self.direction_lookback_seconds

        ma_duration_seconds = self.ma_duration_seconds

        debug_level: Union[Unset, str] = UNSET
        if not isinstance(self.debug_level, Unset):
            debug_level = self.debug_level


        hysteresis_feet = self.hysteresis_feet

        user_defined: Union[Unset, dict[str, Any], str]
        if isinstance(self.user_defined, Unset):
            user_defined = UNSET
        elif isinstance(self.user_defined, DirectionalitySettingsAdvancedConfigUserDefinedType1):
            user_defined = self.user_defined.to_dict()
        else:
            user_defined = self.user_defined

        regression_min_n = self.regression_min_n

        regression_min_duration_seconds = self.regression_min_duration_seconds

        regression_extrapolation_multiplier = self.regression_extrapolation_multiplier

        regression_slope_threshold = self.regression_slope_threshold

        confirm_direction_with_final_zone = self.confirm_direction_with_final_zone

        max_tags_limit = self.max_tags_limit

        raw_location_conf_threshold = self.raw_location_conf_threshold


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if report_new is not UNSET:
            field_dict["report_new"] = report_new
        if report_transition is not UNSET:
            field_dict["report_transition"] = report_transition
        if report_timed_out is not UNSET:
            field_dict["report_timed_out"] = report_timed_out
        if report_direction is not UNSET:
            field_dict["report_direction"] = report_direction
        if report_location_history is not UNSET:
            field_dict["report_location_history"] = report_location_history
        if report_zone_history is not UNSET:
            field_dict["report_zone_history"] = report_zone_history
        if report_update_duration_seconds is not UNSET:
            field_dict["report_update_duration_seconds"] = report_update_duration_seconds
        if report_raw is not UNSET:
            field_dict["report_raw"] = report_raw
        if tag_timeout_seconds_min is not UNSET:
            field_dict["tag_timeout_seconds_min"] = tag_timeout_seconds_min
        if tag_timeout_seconds_default is not UNSET:
            field_dict["tag_timeout_seconds_default"] = tag_timeout_seconds_default
        if tag_timeout_seconds_max is not UNSET:
            field_dict["tag_timeout_seconds_max"] = tag_timeout_seconds_max
        if sigma_multiplier is not UNSET:
            field_dict["sigma_multiplier"] = sigma_multiplier
        if background_processing_interval_seconds is not UNSET:
            field_dict["background_processing_interval_seconds"] = background_processing_interval_seconds
        if direction_lookback_seconds is not UNSET:
            field_dict["direction_lookback_seconds"] = direction_lookback_seconds
        if ma_duration_seconds is not UNSET:
            field_dict["ma_duration_seconds"] = ma_duration_seconds
        if debug_level is not UNSET:
            field_dict["debug_level"] = debug_level
        if hysteresis_feet is not UNSET:
            field_dict["hysteresis_feet"] = hysteresis_feet
        if user_defined is not UNSET:
            field_dict["user_defined"] = user_defined
        if regression_min_n is not UNSET:
            field_dict["regression_min_n"] = regression_min_n
        if regression_min_duration_seconds is not UNSET:
            field_dict["regression_min_duration_seconds"] = regression_min_duration_seconds
        if regression_extrapolation_multiplier is not UNSET:
            field_dict["regression_extrapolation_multiplier"] = regression_extrapolation_multiplier
        if regression_slope_threshold is not UNSET:
            field_dict["regression_slope_threshold"] = regression_slope_threshold
        if confirm_direction_with_final_zone is not UNSET:
            field_dict["confirm_direction_with_final_zone"] = confirm_direction_with_final_zone
        if max_tags_limit is not UNSET:
            field_dict["max_tags_limit"] = max_tags_limit
        if raw_location_conf_threshold is not UNSET:
            field_dict["raw_location_conf_threshold"] = raw_location_conf_threshold

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.directionality_settings_advanced_config_user_defined_type_1 import DirectionalitySettingsAdvancedConfigUserDefinedType1
        d = dict(src_dict)
        report_new = d.pop("report_new", UNSET)

        report_transition = d.pop("report_transition", UNSET)

        report_timed_out = d.pop("report_timed_out", UNSET)

        report_direction = []
        _report_direction = d.pop("report_direction", UNSET)
        for report_direction_item_data in (_report_direction or []):
            report_direction_item = check_directionality_settings_advanced_config_report_direction_item(report_direction_item_data)



            report_direction.append(report_direction_item)


        report_location_history = d.pop("report_location_history", UNSET)

        report_zone_history = d.pop("report_zone_history", UNSET)

        report_update_duration_seconds = d.pop("report_update_duration_seconds", UNSET)

        report_raw = d.pop("report_raw", UNSET)

        tag_timeout_seconds_min = d.pop("tag_timeout_seconds_min", UNSET)

        tag_timeout_seconds_default = d.pop("tag_timeout_seconds_default", UNSET)

        tag_timeout_seconds_max = d.pop("tag_timeout_seconds_max", UNSET)

        sigma_multiplier = d.pop("sigma_multiplier", UNSET)

        background_processing_interval_seconds = d.pop("background_processing_interval_seconds", UNSET)

        direction_lookback_seconds = d.pop("direction_lookback_seconds", UNSET)

        ma_duration_seconds = d.pop("ma_duration_seconds", UNSET)

        _debug_level = d.pop("debug_level", UNSET)
        debug_level: Union[Unset, DirectionalitySettingsAdvancedConfigDebugLevel]
        if isinstance(_debug_level,  Unset):
            debug_level = UNSET
        else:
            debug_level = check_directionality_settings_advanced_config_debug_level(_debug_level)




        hysteresis_feet = d.pop("hysteresis_feet", UNSET)

        def _parse_user_defined(data: object) -> Union['DirectionalitySettingsAdvancedConfigUserDefinedType1', Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_defined_type_1 = DirectionalitySettingsAdvancedConfigUserDefinedType1.from_dict(data)



                return user_defined_type_1
            except: # noqa: E722
                pass
            return cast(Union['DirectionalitySettingsAdvancedConfigUserDefinedType1', Unset, str], data)

        user_defined = _parse_user_defined(d.pop("user_defined", UNSET))


        regression_min_n = d.pop("regression_min_n", UNSET)

        regression_min_duration_seconds = d.pop("regression_min_duration_seconds", UNSET)

        regression_extrapolation_multiplier = d.pop("regression_extrapolation_multiplier", UNSET)

        regression_slope_threshold = d.pop("regression_slope_threshold", UNSET)

        confirm_direction_with_final_zone = d.pop("confirm_direction_with_final_zone", UNSET)

        max_tags_limit = d.pop("max_tags_limit", UNSET)

        raw_location_conf_threshold = d.pop("raw_location_conf_threshold", UNSET)

        directionality_settings_advanced_config = cls(
            report_new=report_new,
            report_transition=report_transition,
            report_timed_out=report_timed_out,
            report_direction=report_direction,
            report_location_history=report_location_history,
            report_zone_history=report_zone_history,
            report_update_duration_seconds=report_update_duration_seconds,
            report_raw=report_raw,
            tag_timeout_seconds_min=tag_timeout_seconds_min,
            tag_timeout_seconds_default=tag_timeout_seconds_default,
            tag_timeout_seconds_max=tag_timeout_seconds_max,
            sigma_multiplier=sigma_multiplier,
            background_processing_interval_seconds=background_processing_interval_seconds,
            direction_lookback_seconds=direction_lookback_seconds,
            ma_duration_seconds=ma_duration_seconds,
            debug_level=debug_level,
            hysteresis_feet=hysteresis_feet,
            user_defined=user_defined,
            regression_min_n=regression_min_n,
            regression_min_duration_seconds=regression_min_duration_seconds,
            regression_extrapolation_multiplier=regression_extrapolation_multiplier,
            regression_slope_threshold=regression_slope_threshold,
            confirm_direction_with_final_zone=confirm_direction_with_final_zone,
            max_tags_limit=max_tags_limit,
            raw_location_conf_threshold=raw_location_conf_threshold,
        )


        directionality_settings_advanced_config.additional_properties = d
        return directionality_settings_advanced_config

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
