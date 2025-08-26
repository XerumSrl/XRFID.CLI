from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.supported_standard_list import SupportedStandardList
from ...models.supported_standardlist import SupportedStandardlist
from typing import cast



def _get_kwargs(
    *,
    body: SupportedStandardList,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/cloud/supportedStandardList",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Error, SupportedStandardlist]]:
    if response.status_code == 200:
        response_200 = SupportedStandardlist.from_dict(response.json())



        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Error, SupportedStandardlist]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SupportedStandardList,

) -> Response[Union[Error, SupportedStandardlist]]:
    """ Retrieves the standard channels of the Supported regions

     based on the region name provided it retrieves the standard channel list

    Args:
        body (SupportedStandardList): Based on the region name provoided it gives the channel list

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SupportedStandardlist]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SupportedStandardList,

) -> Optional[Union[Error, SupportedStandardlist]]:
    """ Retrieves the standard channels of the Supported regions

     based on the region name provided it retrieves the standard channel list

    Args:
        body (SupportedStandardList): Based on the region name provoided it gives the channel list

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SupportedStandardlist]
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SupportedStandardList,

) -> Response[Union[Error, SupportedStandardlist]]:
    """ Retrieves the standard channels of the Supported regions

     based on the region name provided it retrieves the standard channel list

    Args:
        body (SupportedStandardList): Based on the region name provoided it gives the channel list

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Error, SupportedStandardlist]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: SupportedStandardList,

) -> Optional[Union[Error, SupportedStandardlist]]:
    """ Retrieves the standard channels of the Supported regions

     based on the region name provided it retrieves the standard channel list

    Args:
        body (SupportedStandardList): Based on the region name provoided it gives the channel list

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Error, SupportedStandardlist]
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
