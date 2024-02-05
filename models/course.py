from typing import Optional

from pydantic import BaseModel


class CourseCreateSchema(BaseModel):
    name: str
    description: Optional[str]
    author_id: int

    class Config:
        from_attributes = True


class CourseAndUser(BaseModel):
    user_id: int
    course_id: int
