from typing import Any, Unpack

from app.config import settings
from app.integrations.send_request import send_request
from app.interfaces.access_control_service_interface import (
    IAccessControlService,
)


class AccessControlServiceStub(IAccessControlService):
    storage = []
    whitelist = []

    def __init__(self, service_url: str):
        self.__url = service_url
        self.token = settings.VALID_TOKEN

    def __str__(self):
        return "Access Control Service Stub"

    @property
    def url(self):
        return self.__url

    async def login_user(self, user_id: int, user_name: str) -> Any:
        if not user_id in self.storage:
            self.storage.append(user_id)
            return self.token

    async def ban_user(self, user_id: int) -> Any:
        if user_id in self.storage:
            self.storage.remove(user_id)

    async def add_user_to_whitelist(self, user_id: int) -> Any:
        if not user_id in self.whitelist:
            self.whitelist.append(user_id)

    async def ban_user_in_whitelist(self, user_id: int) -> Any:
        if user_id in self.whitelist:
            self.whitelist.remove(user_id)

    async def check_access(self, user_id: int) -> Any:
        return user_id in self.whitelist
