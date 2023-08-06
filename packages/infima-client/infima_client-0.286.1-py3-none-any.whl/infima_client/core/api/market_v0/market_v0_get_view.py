from typing import Any, Dict, List, Optional, Union, cast

import httpx

from infima_client.core.client import Client
from infima_client.core.models.google.rpc.status import GoogleRpcStatus
from infima_client.core.models.market.v0.get_view_request import MarketV0GetViewRequest
from infima_client.core.models.market.v0.get_view_response import (
    MarketV0GetViewResponse,
)
from infima_client.core.types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    json_body: MarketV0GetViewRequest,
) -> Dict[str, Any]:
    url = "{}/api/v0/market/get_view".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[GoogleRpcStatus, MarketV0GetViewResponse]]:
    if response.status_code == 200:
        response_200 = MarketV0GetViewResponse.from_dict(response.json())

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
) -> Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: MarketV0GetViewRequest,
) -> Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]:
    """
    Args:
        json_body (MarketV0GetViewRequest):

    Returns:
        Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: MarketV0GetViewRequest,
) -> Optional[Union[GoogleRpcStatus, MarketV0GetViewResponse]]:
    """
    Args:
        json_body (MarketV0GetViewRequest):

    Returns:
        Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: MarketV0GetViewRequest,
) -> Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]:
    """
    Args:
        json_body (MarketV0GetViewRequest):

    Returns:
        Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: MarketV0GetViewRequest,
) -> Optional[Union[GoogleRpcStatus, MarketV0GetViewResponse]]:
    """
    Args:
        json_body (MarketV0GetViewRequest):

    Returns:
        Response[Union[GoogleRpcStatus, MarketV0GetViewResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
