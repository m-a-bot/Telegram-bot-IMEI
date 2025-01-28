from app.config import settings
from app.integrations.factories import AccessControlServiceBuilder


class WhitelistService:
    def __init__(self):
        self.access_control_service = (
            AccessControlServiceBuilder.build_service(settings)
        )

    async def add_to_whitelist(self, user_id: int):
        await self.access_control_service.add_user_to_whitelist(user_id)

    async def remove_from_whitelist(self, user_id: int):
        await self.access_control_service.ban_user_in_whitelist(user_id)

    async def check_access(self, user_id: int):
        await self.access_control_service.check_access(user_id)
