from typing import List, Optional

from pydantic import BaseModel


class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = False
    roles: List[str] = []
