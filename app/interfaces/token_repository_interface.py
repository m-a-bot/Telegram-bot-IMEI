from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import Unpack


class ITokenRepository(ABC):

    @abstractmethod
    async def add_token(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_token(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_token(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError
