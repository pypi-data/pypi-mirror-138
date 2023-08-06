from typing import Any, Dict, List, Optional, Union, cast

import httpx

from infima_client.core.client import Client
from infima_client.core.models.core.binary_info import CoreBinaryInfo
from infima_client.core.models.google.rpc.status import GoogleRpcStatus
from infima_client.core.types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/api/v0/pricing/get_service_info".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[CoreBinaryInfo, GoogleRpcStatus]]:
    if response.status_code == 200:
        response_200 = CoreBinaryInfo.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = GoogleRpcStatus.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = GoogleRpcStatus.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = GoogleRpcStatus.from_dict(response.json())

        return response_404
    if response.status_code == 408:
        response_408 = GoogleRpcStatus.from_dict(response.json())

        return response_408
    if response.status_code == 500:
        response_500 = GoogleRpcStatus.from_dict(response.json())

        return response_500
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[CoreBinaryInfo, GoogleRpcStatus]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[CoreBinaryInfo, GoogleRpcStatus]]:
    """
    Returns:
        Response[Union[CoreBinaryInfo, GoogleRpcStatus]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[CoreBinaryInfo, GoogleRpcStatus]]:
    """
    Returns:
        Response[Union[CoreBinaryInfo, GoogleRpcStatus]]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[CoreBinaryInfo, GoogleRpcStatus]]:
    """
    Returns:
        Response[Union[CoreBinaryInfo, GoogleRpcStatus]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[CoreBinaryInfo, GoogleRpcStatus]]:
    """
    Returns:
        Response[Union[CoreBinaryInfo, GoogleRpcStatus]]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
