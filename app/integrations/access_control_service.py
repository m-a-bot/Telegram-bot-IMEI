from typing import Any, Unpack
from urllib.parse import urljoin

from aiohttp import ClientResponseError

from app.config import settings
from app.exceptions import AccessDeniedError, UserAlreadyExistsError
from app.integrations.send_request import send_request
from app.interfaces.access_control_service_interface import (
    IAccessControlService,
)


class AccessControlService(IAccessControlService):
    def __init__(self, service_url: str):
        self.__url = service_url

    def __str__(self):
        return "Access Control Service"

    @property
    def url(self):
        return self.__url

    async def login_user(self, user_id: int) -> Any:
        login_user_url = urljoin(self.url, settings.LOGIN_USER_URL)

        try:
            return await send_request(
                endpoint=login_user_url,
                method="POST",
                query_params={"user_id": user_id},
            )
        except ClientResponseError as exc:
            if exc.status == 409:
                raise UserAlreadyExistsError from exc

    async def ban_user(self, user_id: int) -> Any:
        ban_user_url = urljoin(self.url, settings.BAN_USER_URL)

        await send_request(
            endpoint=ban_user_url,
            method="DELETE",
            query_params={
                "user_id": user_id,
            },
        )

    async def add_user_to_whitelist(self, user_id: int, user_name: str) -> Any:
        add_user_to_whitelist_url = urljoin(
            self.url, settings.ADD_USER_TO_WHITELIST_URL
        )

        try:
            await send_request(
                endpoint=add_user_to_whitelist_url,
                method="POST",
                query_params={"user_id": user_id, "user_name": user_name},
            )
        except ClientResponseError as exc:
            if exc.status == 409:
                raise UserAlreadyExistsError from exc

    async def ban_user_in_whitelist(self, user_id: int) -> Any:
        ban_user_in_whitelist_url = urljoin(
            self.url, settings.BAN_USER_IN_WHITELIST_URL
        )

        await send_request(
            endpoint=ban_user_in_whitelist_url,
            method="DELETE",
            query_params={
                "user_id": user_id,
            },
        )

    async def check_access(self, user_id: int) -> Any:
        check_access_url = urljoin(self.url, settings.CHECK_ACCESS_URL)

        try:
            await send_request(
                endpoint=check_access_url,
                method="GET",
                query_params={
                    "user_id": user_id,
                },
            )
        except ClientResponseError as exc:
            if exc.status == 403:
                raise AccessDeniedError from exc
