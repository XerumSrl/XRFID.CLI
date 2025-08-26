from typing import Literal, cast

SetInstallUserappBodyAuthenticationType = Literal['BASIC', 'NONE']

SET_INSTALL_USERAPP_BODY_AUTHENTICATION_TYPE_VALUES: set[SetInstallUserappBodyAuthenticationType] = { 'BASIC', 'NONE',  }

def check_set_install_userapp_body_authentication_type(value: str) -> SetInstallUserappBodyAuthenticationType:
    if value in SET_INSTALL_USERAPP_BODY_AUTHENTICATION_TYPE_VALUES:
        return cast(SetInstallUserappBodyAuthenticationType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SET_INSTALL_USERAPP_BODY_AUTHENTICATION_TYPE_VALUES!r}")
