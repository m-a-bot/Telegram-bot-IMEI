from app.config import settings
from app.integrations.factories import CheckIMEIServiceBuilder
from app.schemas.pyd import IMEICheck


class IMEIValidationService:
    def __init__(self):
        self.check_imei_service = CheckIMEIServiceBuilder.build_service(
            settings
        )

    async def verify_imei(self, imei: str, token: str, user_id: int):
        imei_check = IMEICheck(deviceId=imei, serviceId=settings.SERVICE_ID)
        return await self.check_imei_service.check_imei(
            imei_check, token, user_id
        )
