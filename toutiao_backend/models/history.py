from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models.users import Base as UserBase


class History(UserBase):
    """浏览记录表 ORM 模型"""
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    news_id: Mapped[int] = mapped_column(Integer, nullable=False)
    view_time: Mapped[datetime] = mapped_column(
        DateTime, insert_default=func.now(), comment="浏览时间"
    )

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"













