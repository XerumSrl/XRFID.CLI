from typing import Literal, cast

AZUREAdditionalQos = Literal[0, 1, 2]

AZURE_ADDITIONAL_QOS_VALUES: set[AZUREAdditionalQos] = { 0, 1, 2,  }

def check_azure_additional_qos(value: int) -> AZUREAdditionalQos:
    if value in AZURE_ADDITIONAL_QOS_VALUES:
        return cast(AZUREAdditionalQos, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AZURE_ADDITIONAL_QOS_VALUES!r}")
