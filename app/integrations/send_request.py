import json
import logging
from typing import Any, Optional

import aiohttp
from aiohttp import ClientError, ClientResponseError


async def send_request(
    endpoint: str,
    method: str,
    query_params: Optional[dict] = None,
    data: Optional[str | bytes | dict] = None,
    headers: Optional[dict] = None,
    verify_ssl: bool = False,
) -> Any:
    """Sends an HTTP request to the specified endpoint"""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=endpoint,
                params=(
                    {p: v for p, v in query_params.items() if v is not None}
                    if query_params
                    else None
                ),
                data=data,
                headers=headers,
                ssl=verify_ssl,
            ) as response:
                response.raise_for_status()

                return await response.json()
    except ClientResponseError as exc:
        logging.error(
            f"Error during {method} request to {endpoint}, status code: {exc.status}, message: {exc.message}",
            exc_info=exc,
        )
        raise exc

    except ClientError as exc:
        logging.error(
            f"Client Error during {method} request to {endpoint}", exc_info=exc
        )
        raise exc

    except json.JSONDecodeError as exc:
        logging.error(
            f"Error decoding JSON for {method} request to {endpoint}",
            exc_info=exc,
        )
        raise exc

    except Exception as exc:
        logging.error(
            f"Unexpected error during {method} request to {endpoint}",
            exc_info=exc,
        )
        raise exc
