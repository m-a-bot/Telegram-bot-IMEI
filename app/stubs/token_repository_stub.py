from app.interfaces.token_repository_interface import ITokenRepository


class TokenRepositoryStub(ITokenRepository):
    storage: dict[int, str] = {}

    def __init__(self, session):
        self._session = session

    async def add_token(self, user_id: int, token: str):
        self.storage[user_id] = token

    async def get_token(self, user_id: int):
        return self.storage.get(user_id)

    async def delete_token(self, user_id: int):
        token = self.storage.get(user_id)
        if token:
            self.storage.pop(user_id)
