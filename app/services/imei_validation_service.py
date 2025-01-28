from app.config import settings
from app.integrations.factories import CheckIMEIServiceBuilder


class IMEIValidationService:
    def __init__(self):
        self.check_imei_service = CheckIMEIServiceBuilder.build_service(
            settings
        )

    async def verify_imei(self, imei: str, token: str, user_id: int):
        return await self.check_imei_service.check_imei(
            imei, token, user_id, settings.SERVICE_ID
        )
