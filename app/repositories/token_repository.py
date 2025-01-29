from redis.asyncio import Redis

from app.config import settings
from app.interfaces.token_repository_interface import ITokenRepository

TOKENS_KEY = "user_tokens"


class TokenRepository(ITokenRepository):
    def __init__(self, session):
        self._session: Redis = session

    async def add_token(self, user_id: int, token: str):
        user_key = f"{TOKENS_KEY}:{user_id}"
        result = await self._session.set(
            user_key,
            token,
            ex=settings.TOKEN_TTL - settings.BUFFER_TTL,
            nx=True,
        )
        return result

    async def delete_token(self, user_id):
        if await self.get_token(user_id) is None:
            return None

        user_key = f"{TOKENS_KEY}:{user_id}"
        return await self._session.delete(user_key)

    async def get_token(self, user_id: int):
        user_key = f"{TOKENS_KEY}:{user_id}"
        return await self._session.get(user_key)
