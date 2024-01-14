from _datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, TIMESTAMP, Boolean

from enums.color import EColorSchema
from enums.font import EFontSize

metadata = MetaData()

difficulty = Table(
    'difficulty',
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False)
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("middle_name", String, nullable=False),
    Column("role", String, nullable=False),
    Column("status", String, nullable=True),
    Column("email", String, nullable=False),
    Column("password", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow)
)

user_settings = Table(
    "user_settings",
    metadata,
    Column("color_schema", String, default=EColorSchema.DEFAULT),
    Column("font_size", String, default=EFontSize.DEFAULT),
    Column("icon_presence", Boolean, default=True),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False)
)

course = Table(
    "course",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("author_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("initial_test_id", Integer, nullable=True)
)

course_theme = Table(
    "course_theme",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("course_id", Integer, ForeignKey("course.id"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow)
)

course_theme_item = Table(
    "course_theme_item",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("course_theme_id", Integer, ForeignKey("course_theme.id"), nullable=False),
    Column("difficulty_id", Integer, ForeignKey("difficulty.id"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("file_uuid", String, nullable=True)
)

test = Table(
    "test",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("course_theme_item_id", Integer, ForeignKey("course_theme_item.id"), nullable=False),
    Column("is_auth_test", Boolean, default=False),
)

test_question = Table(
    "test_question",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("test_id", Integer, ForeignKey("test.id"), nullable=False),
    Column("picture_uuid", String, nullable=True),
    Column("index", Integer, nullable=False)
)

test_question_answer = Table(
    "test_question_answer",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("is_correct", Boolean, nullable=False),
    Column("test_question_id", Integer, ForeignKey("test_question.id"), nullable=False),
    Column("picture_uuid", String, nullable=True),
    Column("index", Integer, nullable=False)
)

test_result = Table(
    "test_result",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP, nullable=False, default=datetime.utcnow),
    Column("test_id", Integer, ForeignKey("test.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("result", Integer, nullable=False),
    Column("avg_answer_time", Integer, nullable=False),
    Column("time_spent", Integer, nullable=False),  # в секундах
)
