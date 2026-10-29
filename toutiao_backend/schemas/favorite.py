from pydantic import BaseModel, ConfigDict, Field


class FavoriteAddRequest(BaseModel):
    """
    前端提交的是 { newsId }，用 alias 兼容驼峰写法。
    populate_by_name 让下划线写法 news_id 也能用。
    """
    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(alias="newsId")


class FavoriteItemResponse(BaseModel):
    """
    收藏列表里的一条记录（扁平结构）。
    前端 Favorite.vue 直接取 item.id / item.title / item.image /
    item.author / item.publishTime / item.favoriteTime，
    其中 item.id 是新闻ID（用于跳转详情、取消收藏）。
    """
    id: int
    title: str
    image: str | None = None
    description: str | None = None
    publish_time: str | None = Field(default=None, serialization_alias="publishTime")
    author: str | None = None
    views: int = 0
    favorite_time: str | None = Field(default=None, serialization_alias="favoriteTime")
