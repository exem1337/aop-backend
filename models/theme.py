from typing import Optional

from pydantic import BaseModel


class ThemeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: int
