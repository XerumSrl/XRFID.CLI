from typing import Literal, cast

SetUpdateCertificateType = Literal['app', 'client', 'server']

SET_UPDATE_CERTIFICATE_TYPE_VALUES: set[SetUpdateCertificateType] = { 'app', 'client', 'server',  }

def check_set_update_certificate_type(value: str) -> SetUpdateCertificateType:
    if value in SET_UPDATE_CERTIFICATE_TYPE_VALUES:
        return cast(SetUpdateCertificateType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SET_UPDATE_CERTIFICATE_TYPE_VALUES!r}")
