from typing import Literal, cast

AWSAdditionalQos = Literal[0, 1, 2]

AWS_ADDITIONAL_QOS_VALUES: set[AWSAdditionalQos] = { 0, 1, 2,  }

def check_aws_additional_qos(value: int) -> AWSAdditionalQos:
    if value in AWS_ADDITIONAL_QOS_VALUES:
        return cast(AWSAdditionalQos, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {AWS_ADDITIONAL_QOS_VALUES!r}")
