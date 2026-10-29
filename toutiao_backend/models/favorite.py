from datetime import datetime

from sqlalchemy import DateTime, Index, Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.users import Base as UserBase


class Favorite(UserBase):
    """收藏表ORM模型"""
    __tablename__ = "favorite"

    __table_args__ = (
        Index("user_news_unique", "user_id", "news_id", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    news_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
