from app.config import Settings
from app.repositories.token_repository import TokenRepository
from app.stubs.token_repository_stub import TokenRepositoryStub


class TokenRepositoryBuilder:
    @staticmethod
    def build_service(session, settings: Settings):
        if "test" in settings.ACCESS_CONTROL_URL:
            return TokenRepositoryStub(None)
        else:
            return TokenRepository(session)
