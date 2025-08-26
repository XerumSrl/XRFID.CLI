from typing import Literal, cast

SetRefreshCertificateBodyType = Literal['app', 'client', 'server']

SET_REFRESH_CERTIFICATE_BODY_TYPE_VALUES: set[SetRefreshCertificateBodyType] = { 'app', 'client', 'server',  }

def check_set_refresh_certificate_body_type(value: str) -> SetRefreshCertificateBodyType:
    if value in SET_REFRESH_CERTIFICATE_BODY_TYPE_VALUES:
        return cast(SetRefreshCertificateBodyType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SET_REFRESH_CERTIFICATE_BODY_TYPE_VALUES!r}")
