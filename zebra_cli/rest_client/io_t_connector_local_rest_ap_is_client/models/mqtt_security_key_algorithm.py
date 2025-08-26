from typing import Literal, cast

MQTTSecurityKeyAlgorithm = Literal['RSA256']

MQTT_SECURITY_KEY_ALGORITHM_VALUES: set[MQTTSecurityKeyAlgorithm] = { 'RSA256',  }

def check_mqtt_security_key_algorithm(value: str) -> MQTTSecurityKeyAlgorithm:
    if value in MQTT_SECURITY_KEY_ALGORITHM_VALUES:
        return cast(MQTTSecurityKeyAlgorithm, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MQTT_SECURITY_KEY_ALGORITHM_VALUES!r}")
