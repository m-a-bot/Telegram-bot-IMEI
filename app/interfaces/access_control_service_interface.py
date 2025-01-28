from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import Unpack


class IAccessControlService(ABC):
    @abstractmethod
    async def login_user(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def ban_user(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def add_user_to_whitelist(
        self, *args: Unpack[Any], **kwargs: Any
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def ban_user_in_whitelist(
        self, *args: Unpack[Any], **kwargs: Any
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def check_access(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError
