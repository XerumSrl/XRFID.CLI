from typing import Literal, cast

DelCertificateBodyType = Literal['app', 'client']

DEL_CERTIFICATE_BODY_TYPE_VALUES: set[DelCertificateBodyType] = { 'app', 'client',  }

def check_del_certificate_body_type(value: str) -> DelCertificateBodyType:
    if value in DEL_CERTIFICATE_BODY_TYPE_VALUES:
        return cast(DelCertificateBodyType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEL_CERTIFICATE_BODY_TYPE_VALUES!r}")
