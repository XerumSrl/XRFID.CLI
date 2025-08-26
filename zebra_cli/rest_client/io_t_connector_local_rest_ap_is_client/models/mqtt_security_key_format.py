from typing import Literal, cast

MQTTSecurityKeyFormat = Literal['PEM']

MQTT_SECURITY_KEY_FORMAT_VALUES: set[MQTTSecurityKeyFormat] = { 'PEM',  }

def check_mqtt_security_key_format(value: str) -> MQTTSecurityKeyFormat:
    if value in MQTT_SECURITY_KEY_FORMAT_VALUES:
        return cast(MQTTSecurityKeyFormat, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MQTT_SECURITY_KEY_FORMAT_VALUES!r}")
