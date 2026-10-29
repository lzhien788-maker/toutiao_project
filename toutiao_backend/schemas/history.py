from pydantic import BaseModel, ConfigDict, Field


class HistoryAddRequest(BaseModel):
    """
    记录浏览历史的请求体，前端提交 { newsId }
    用 alias 兼容驼峰写法，populate_by_name 让下划线写法也能用
    """
    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(alias="newsId")


class HistoryItemResponse(BaseModel):
    """
    浏览历史列表里的一条记录（扁平结构）。
    前端 History.vue 直接取 item.id / item.title / item.image /
    item.author / item.publishTime / item.viewTime，
    其中 item.id 是新闻ID（用于跳转详情、删除这条记录）。
    """
    id: int
    title: str
    image: str | None = None
    description: str | None = None
    publish_time: str | None = Field(default=None, serialization_alias="publishTime")
    author: str | None = None
    views: int = 0
    view_time: str | None = Field(default=None, serialization_alias="viewTime")
