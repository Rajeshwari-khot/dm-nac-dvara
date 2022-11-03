from pydantic import BaseModel
from typing import Optional


class LogBase(BaseModel):
    channel: Optional[str]
    request_url: Optional[str]
    request_method: Optional[str]
    params: Optional[str]
    request_body: Optional[str]
    response_body: Optional[str]
    status_code: Optional[str]
    api_call_duration: Optional[str]
    request_time: Optional[str]

