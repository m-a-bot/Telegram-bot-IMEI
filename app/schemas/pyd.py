from typing import List, Literal

from pydantic import BaseModel


class IMEICheck(BaseModel):
    deviceId: str
    serviceId: int
