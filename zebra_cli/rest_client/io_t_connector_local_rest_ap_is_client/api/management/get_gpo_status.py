from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_gpo_status_response_200 import GetGpoStatusResponse200
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cloud/gpo",
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, GetGpoStatusResponse200]]:
    if response.status_code == 200:
        response_200 = GetGpoStatusResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, GetGpoStatusResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Error, GetGpoStatusResponse200]]:
    """ Get GPO Status

     Retrieves the GPO status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 3 GPO pins
    2. FX9600 = 4 GPO pins
    3. ATR7000 = 3 GPO pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetGpoStatusResponse200]]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[Error, GetGpoStatusResponse200]]:
    """ Get GPO Status

     Retrieves the GPO status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 3 GPO pins
    2. FX9600 = 4 GPO pins
    3. ATR7000 = 3 GPO pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetGpoStatusResponse200]
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Error, GetGpoStatusResponse200]]:
    """ Get GPO Status

     Retrieves the GPO status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 3 GPO pins
    2. FX9600 = 4 GPO pins
    3. ATR7000 = 3 GPO pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetGpoStatusResponse200]]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[Error, GetGpoStatusResponse200]]:
    """ Get GPO Status

     Retrieves the GPO status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 3 GPO pins
    2. FX9600 = 4 GPO pins
    3. ATR7000 = 3 GPO pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetGpoStatusResponse200]
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
