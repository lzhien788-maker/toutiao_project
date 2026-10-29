from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==================== 分类 ====================

class CategoryResponse(BaseModel):
    """分类响应体 — 用于序列化 Category ORM 对象"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sort_order: int = Field(serialization_alias="sortOrder")


# ==================== 新闻 ====================

class NewsResponse(BaseModel):
    """
    新闻简略信息响应体 — 用于新闻列表
    前端 NewsItem.vue 用的是 news.publishTime / news.categoryId（驼峰），
    所以用 serialization_alias 把下划线字段转成驼峰输出。
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(serialization_alias="categoryId")
    views: int = 0
    # ORM 里是 datetime，schema 也声明成 datetime，让 Pydantic 能 model_validate 通过
    # 路由里 model_dump() 后手动 str() 化成字符串返回给前端
    publish_time: Optional[datetime] = Field(default=None, serialization_alias="publishTime")


class NewsDetailResponse(BaseModel):
    """新闻详情响应体 — 用于新闻详情"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    content: str
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(serialization_alias="categoryId")
    views: int = 0
    publish_time: Optional[datetime] = Field(default=None, serialization_alias="publishTime")
