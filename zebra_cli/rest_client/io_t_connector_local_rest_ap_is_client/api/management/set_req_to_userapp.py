from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.set_req_to_userapp_body import SetReqToUserappBody
from ...models.set_req_to_userapp_response_200 import SetReqToUserappResponse200
from typing import cast



def _get_kwargs(
    appname: str,
    *,
    body: SetReqToUserappBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/cloud/apps/{appname}/pass-through".format(appname=appname,),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, SetReqToUserappResponse200]]:
    if response.status_code == 200:
        response_200 = SetReqToUserappResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, SetReqToUserappResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    appname: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetReqToUserappBody,

) -> Response[Union[Error, SetReqToUserappResponse200]]:
    """ Send Request to Userapp

     sending request to uers application

    Args:
        appname (str):  Example: sample.
        body (SetReqToUserappBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SetReqToUserappResponse200]]
     """


    kwargs = _get_kwargs(
        appname=appname,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    appname: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetReqToUserappBody,

) -> Optional[Union[Error, SetReqToUserappResponse200]]:
    """ Send Request to Userapp

     sending request to uers application

    Args:
        appname (str):  Example: sample.
        body (SetReqToUserappBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SetReqToUserappResponse200]
     """


    return sync_detailed(
        appname=appname,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    appname: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetReqToUserappBody,

) -> Response[Union[Error, SetReqToUserappResponse200]]:
    """ Send Request to Userapp

     sending request to uers application

    Args:
        appname (str):  Example: sample.
        body (SetReqToUserappBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SetReqToUserappResponse200]]
     """


    kwargs = _get_kwargs(
        appname=appname,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    appname: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: SetReqToUserappBody,

) -> Optional[Union[Error, SetReqToUserappResponse200]]:
    """ Send Request to Userapp

     sending request to uers application

    Args:
        appname (str):  Example: sample.
        body (SetReqToUserappBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SetReqToUserappResponse200]
     """


    return (await asyncio_detailed(
        appname=appname,
client=client,
body=body,

    )).parsed
