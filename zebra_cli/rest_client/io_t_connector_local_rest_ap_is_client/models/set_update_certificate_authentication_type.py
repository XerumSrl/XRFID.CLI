from typing import Literal, cast

SetUpdateCertificateAuthenticationType = Literal['BASIC', 'NONE']

SET_UPDATE_CERTIFICATE_AUTHENTICATION_TYPE_VALUES: set[SetUpdateCertificateAuthenticationType] = { 'BASIC', 'NONE',  }

def check_set_update_certificate_authentication_type(value: str) -> SetUpdateCertificateAuthenticationType:
    if value in SET_UPDATE_CERTIFICATE_AUTHENTICATION_TYPE_VALUES:
        return cast(SetUpdateCertificateAuthenticationType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SET_UPDATE_CERTIFICATE_AUTHENTICATION_TYPE_VALUES!r}")
