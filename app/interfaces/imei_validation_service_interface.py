from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import Unpack


class ICheckIMEIService(ABC):
    @abstractmethod
    async def check_imei(self, *args: Unpack[Any], **kwargs: Any) -> Any:
        raise NotImplementedError
