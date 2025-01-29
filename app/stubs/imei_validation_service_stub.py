from typing import Any, Unpack

from app.config import settings
from app.integrations.send_request import send_request
from app.interfaces.access_control_service_interface import (
    IAccessControlService,
)
from app.interfaces.imei_validation_service_interface import ICheckIMEIService
from app.schemas.pyd import IMEICheck


class CheckIMEIServiceStub(ICheckIMEIService):
    def __init__(self, service_url: str):
        self.__url = service_url
        self.valid_token = settings.VALID_TOKEN

    def __str__(self):
        return "Check IMEI Service Stub"

    @property
    def url(self):
        return self.__url

    async def check_imei(
        self, imei_check: IMEICheck, token: str, user_id: int
    ) -> Any:
        if len(imei_check.deviceId) == 15 and token == self.valid_token:
            return {
                "success": True,
                "error": "Only Apple devices supported. This device is a NA.",
                "status": "Rejected",
            }
