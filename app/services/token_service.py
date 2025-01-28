from app.config import settings
from app.integrations.factories import AccessControlServiceBuilder
from app.repositories.factories import TokenRepositoryBuilder
from app.repositories.token_repository import TokenRepository


class TokenService:
    def __init__(self, session):
        self._session = session
        self._repository = TokenRepositoryBuilder.build_service(
            self._session, settings
        )
        self.access_control_service = (
            AccessControlServiceBuilder.build_service(settings)
        )

    async def get_token(self, user_id: int):
        token = await self.access_control_service.login_user(
            user_id
        )
        await self._save_token(user_id, token)
        return token

    async def load_token(self, user_id: int):
        token = await self._repository.get_token(user_id)
        return token

    async def _save_token(self, user_id: int, token: str):
        await self._repository.add_token(user_id, token)

    async def delete_token(self, user_id: int):
        await self._repository.delete_token(user_id)
