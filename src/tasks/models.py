from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, UniqueConstraint, Index, func

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    type = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("title", name="uq_task_title"),
        Index("ix_task_type", "type"),
    )

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', type='{self.type}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "type": self.type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
