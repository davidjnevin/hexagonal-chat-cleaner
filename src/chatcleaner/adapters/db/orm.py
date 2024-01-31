from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import registry

from chatcleaner.domain.model import model

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

cleaning = Table(
    "cleaning",
    mapper_registry.metadata,
    Column(
        "id",
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    ),
    Column("uuid", String, unique=True, nullable=False),
    Column("chat_text", String, nullable=False),
    Column("cleaned_chat", String, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
    UniqueConstraint("uuid", name="uuid_unique_constraint"),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Cleaning, cleaning)
