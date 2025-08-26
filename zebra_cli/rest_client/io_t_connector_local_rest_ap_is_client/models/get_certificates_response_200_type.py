from typing import Literal, cast

GetCertificatesResponse200Type = Literal['app', 'client', 'server']

GET_CERTIFICATES_RESPONSE_200_TYPE_VALUES: set[GetCertificatesResponse200Type] = { 'app', 'client', 'server',  }

def check_get_certificates_response_200_type(value: str) -> GetCertificatesResponse200Type:
    if value in GET_CERTIFICATES_RESPONSE_200_TYPE_VALUES:
        return cast(GetCertificatesResponse200Type, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_CERTIFICATES_RESPONSE_200_TYPE_VALUES!r}")
