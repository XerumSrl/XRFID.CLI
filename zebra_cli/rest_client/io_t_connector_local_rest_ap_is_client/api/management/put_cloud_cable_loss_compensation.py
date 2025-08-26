from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.all_ import All
from ...models.each import Each
from ...models.error import Error
from typing import cast
from typing import cast, Union



def _get_kwargs(
    *,
    body: Union['All', 'Each'],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/cloud/cableLossCompensation",
    }

    _kwargs["json"]: dict[str, Any]
    if isinstance(body, All):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body.to_dict()



    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, Error]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
        return response_200
    if response.status_code == 422:
        response_422 = cast(Any, None)
        return response_422
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union['All', 'Each'],

) -> Response[Union[Any, Error]]:
    """ PUT cableLossCompensation

     Sets the Reader Cable Loss Compensation. Includes Cable Length and Cable Loss per Hundred Feet

    Args:
        body (Union['All', 'Each']): Sets the Reader Cable Loss Compensation. Includes Cable
            Length and Cable Loss per Hundred Feet

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
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
    body: Union['All', 'Each'],

) -> Optional[Union[Any, Error]]:
    """ PUT cableLossCompensation

     Sets the Reader Cable Loss Compensation. Includes Cable Length and Cable Loss per Hundred Feet

    Args:
        body (Union['All', 'Each']): Sets the Reader Cable Loss Compensation. Includes Cable
            Length and Cable Loss per Hundred Feet

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union['All', 'Each'],

) -> Response[Union[Any, Error]]:
    """ PUT cableLossCompensation

     Sets the Reader Cable Loss Compensation. Includes Cable Length and Cable Loss per Hundred Feet

    Args:
        body (Union['All', 'Each']): Sets the Reader Cable Loss Compensation. Includes Cable
            Length and Cable Loss per Hundred Feet

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error]]
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
    body: Union['All', 'Each'],

) -> Optional[Union[Any, Error]]:
    """ PUT cableLossCompensation

     Sets the Reader Cable Loss Compensation. Includes Cable Length and Cable Loss per Hundred Feet

    Args:
        body (Union['All', 'Each']): Sets the Reader Cable Loss Compensation. Includes Cable
            Length and Cable Loss per Hundred Feet

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error]
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
