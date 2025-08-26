from typing import Literal, cast

HTTPPostSecurityAuthenticationType = Literal['BASIC', 'NONE', 'TLS-Client']

HTTP_POST_SECURITY_AUTHENTICATION_TYPE_VALUES: set[HTTPPostSecurityAuthenticationType] = { 'BASIC', 'NONE', 'TLS-Client',  }

def check_http_post_security_authentication_type(value: str) -> HTTPPostSecurityAuthenticationType:
    if value in HTTP_POST_SECURITY_AUTHENTICATION_TYPE_VALUES:
        return cast(HTTPPostSecurityAuthenticationType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {HTTP_POST_SECURITY_AUTHENTICATION_TYPE_VALUES!r}")
