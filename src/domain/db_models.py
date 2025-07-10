import uuid
from sqlalchemy import (
    Table,
    Column,
    String,
    MetaData,
    TIMESTAMP,
    func,
    ForeignKey,
    Enum,
    text,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

user_table = Table(
    "user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("full_name", String, nullable=False),
    Column("created_at", TIMESTAMP, server_default=func.now()),
)

task_list_table = Table(
    "task_list",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("name", String, nullable=False),
    Column("created_at", TIMESTAMP, server_default=func.now()),
)

task_priority_enum = Enum(
    "low", "medium", "high", name="task_priority", metadata=metadata
)

task_status_enum = Enum(
    "pending", "in_process", "completed", name="task_status", metadata=metadata
)

task_table = Table(
    "task",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column("title", String, nullable=False),
    Column("priority", task_priority_enum, nullable=False, default="medium"),
    Column("status", task_status_enum, nullable=False, default="pending"),
    Column("completed_percentage", Integer, nullable=True),
    Column(
        "task_list_id",
        UUID(as_uuid=True),
        ForeignKey("task_list.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("created_at", TIMESTAMP, server_default=func.now()),
)

assigned_task = Table(
    "assigned_task",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    ),
    Column(
        "task_id",
        UUID(as_uuid=True),
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("created_at", TIMESTAMP, server_default=func.now()),
)
