from typing import Any, Unpack
from urllib.parse import urljoin

from aiohttp import ClientResponseError

from app.config import settings
from app.exceptions import AccessDeniedError, InvalidDataError
from app.integrations.send_request import send_request
from app.interfaces.access_control_service_interface import (
    IAccessControlService,
)
from app.interfaces.imei_validation_service_interface import ICheckIMEIService
from app.schemas.pyd import IMEICheck


class CheckIMEIService(ICheckIMEIService):
    def __init__(self, service_url: str):
        self.__url = service_url

    def __str__(self):
        return "Check IMEI Service"

    @property
    def url(self):
        return self.__url

    async def check_imei(
        self, imei_check: IMEICheck, token: str, user_id: int
    ) -> dict:
        check_imei_url = urljoin(self.url, settings.CHECK_IMEI_URL)
        payload = imei_check.model_dump_json()

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            return await send_request(
                endpoint=check_imei_url,
                method="POST",
                query_params={"token": token, "user_id": user_id},
                data=payload,
                headers=headers,
            )
        except ClientResponseError as exc:
            if exc.status == 401:
                raise AccessDeniedError from exc
            if exc.status == 422:
                raise InvalidDataError from exc
