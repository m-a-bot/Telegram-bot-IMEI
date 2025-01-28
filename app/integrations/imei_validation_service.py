from typing import Any, Unpack
from urllib.parse import urljoin

from app.config import settings
from app.integrations.send_request import send_request
from app.interfaces.access_control_service_interface import (
    IAccessControlService,
)
from app.interfaces.imei_validation_service_interface import ICheckIMEIService


class CheckIMEIService(ICheckIMEIService):
    def __init__(self, service_url: str):
        self.__url = service_url

    def __str__(self):
        return "Check IMEI Service"

    @property
    def url(self):
        return self.__url

    async def check_imei(
        self, imei: str, token: str, user_id: int, service_id: int = 14
    ) -> dict:
        check_imei_url = urljoin(self.url, settings.CHECK_IMEI_URL)

        result = await send_request(
            endpoint=check_imei_url,
            method="POST",
            query_params={"token": token, "user_id": user_id},
            data={"deviceId": imei, "serviceId": service_id},
        )
        return result
