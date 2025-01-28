from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    WEB_SERVER_HOST: str = "0.0.0.0"
    WEB_SERVER_PORT: int = 8443

    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str
    BASE_WEBHOOK_URL: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_USER_PASSWORD: str

    LOGIN_USER_URL: str = "/login_user"
    BAN_USER_URL: str = "/ban_user"
    ADD_USER_TO_WHITELIST_URL: str = "/whitelist/add_user"
    BAN_USER_IN_WHITELIST_URL: str = "/whitelist/ban_user"
    CHECK_ACCESS_URL: str = "/whitelist/check_access"
    CHECK_IMEI_URL: str = "/api/check-imei"

    ACCESS_CONTROL_URL: str
    CHECK_IMEI_SERVICE_URL: str

    SERVICE_ID: int
    VALID_TOKEN: str
    TOKEN_TTL: int = 3600
    BUFFER_TTL: int = 5

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
