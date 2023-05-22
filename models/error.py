from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4, UUID

class ErrorModel(BaseModel):
    request_id: UUID = uuid4()
    error_message: str