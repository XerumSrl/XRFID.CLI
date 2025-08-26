from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_gpi_status_response_200 import GetGpiStatusResponse200
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cloud/gpi",
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, GetGpiStatusResponse200]]:
    if response.status_code == 200:
        response_200 = GetGpiStatusResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, GetGpiStatusResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Error, GetGpiStatusResponse200]]:
    """ Get GPI Status

     Retrieves the GPI status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 2 GPI pins
    2. FX9600 = 4 GPI pins
    3. ATR7000 = 2 GPI pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetGpiStatusResponse200]]
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

) -> Optional[Union[Error, GetGpiStatusResponse200]]:
    """ Get GPI Status

     Retrieves the GPI status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 2 GPI pins
    2. FX9600 = 4 GPI pins
    3. ATR7000 = 2 GPI pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetGpiStatusResponse200]
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Error, GetGpiStatusResponse200]]:
    """ Get GPI Status

     Retrieves the GPI status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 2 GPI pins
    2. FX9600 = 4 GPI pins
    3. ATR7000 = 2 GPI pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, GetGpiStatusResponse200]]
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

) -> Optional[Union[Error, GetGpiStatusResponse200]]:
    """ Get GPI Status

     Retrieves the GPI status

    Note : 
    Maximum number of ports available per device type
    1. FX7500 = 2 GPI pins
    2. FX9600 = 4 GPI pins
    3. ATR7000 = 2 GPI pins

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, GetGpiStatusResponse200]
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
