from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import news as news_crud
from cache import build_key, get_json_cache, set_json_cache
from schemas.news import CategoryResponse, NewsResponse, NewsDetailResponse
from utils.response import success_response

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    旁路缓存（Cache-Aside）：
      1. 先查 Redis → 有就直接返回
      2. 没有 → 查 DB → ORM → Pydantic dict → 写缓存 → 返回
    分类数据几乎不变，缓存 24h
    """
    cache_key = build_key("news", "categories")
    cached = await get_json_cache(cache_key)
    if cached is not None:
        return success_response(message="获取新闻分类成功", data=cached)

    # 查 DB 拿到 ORM 对象列表
    orm_list = await news_crud.get_categories(db, skip, limit)

    # ★ 关键修复：ORM → Pydantic model → dict（列表推导式转每个对象）
    # by_alias=True：把 category_id/sort_order 输出成 categoryId/sortOrder
    categories = [
        CategoryResponse.model_validate(c).model_dump(by_alias=True)
        for c in orm_list
    ]

    await set_json_cache(cache_key, categories, expire_seconds=86400)
    return success_response(message="获取新闻分类成功", data=categories)


@router.get("/list")
async def get_news(
    category_id: int = Query(..., alias="categoryId"),
    page: int = 1,
    page_size: int = Query(10, le=100, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """
    新闻列表缓存：
      key = toutiao:news:list:{category_id}:{page}:{page_size}
      不同分类、不同页码各自独立缓存 15 分钟
    """
    cache_key = build_key("news", "list", category_id, page, page_size)
    cached = await get_json_cache(cache_key)
    if cached is not None:
        return success_response(
            message="获取新闻列表成功",
            data=cached,
        )

    offset = (page - 1) * page_size
    orm_news_list = await news_crud.get_news_list(db, category_id, offset, page_size)
    total = await news_crud.get_news_count(db, category_id)
    has_more = (offset + len(orm_news_list)) < total

    # ★ ORM 列表 → dict 列表（publish_time 单独 str 化）
    news_list = []
    for n in orm_news_list:
        d = NewsResponse.model_validate(n).model_dump(by_alias=True)
        d["publishTime"] = str(n.publish_time) if n.publish_time else None
        news_list.append(d)

    result = {"list": news_list, "total": total, "hasMore": has_more}
    await set_json_cache(cache_key, result, expire_seconds=900)  # 15分钟
    return success_response(message="获取新闻列表成功", data=result)


@router.get("/detail")
async def read_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    """
    新闻详情缓存：
      浏览量无论命中与否都 +1
      缓存没命中 → 完整查一次 + 写缓存
    详情内容偶尔编辑，缓存 30 分钟
    """
    await news_crud.increase_news_view(db, news_id)

    cache_key = build_key("news", "detail", news_id)
    cached = await get_json_cache(cache_key)
    if cached is not None:
        return success_response(data=cached)

    news_orm = await news_crud.get_news_detail(db, news_id)
    if not news_orm:
        raise HTTPException(status_code=404, detail="新闻不存在")

    related_orm_list = await news_crud.get_related_news(db, news_orm.id, news_orm.category_id)

    # ★ ORM → dict
    related_news = []
    for n in related_orm_list:
        d = NewsResponse.model_validate(n).model_dump(by_alias=True)
        d["publishTime"] = str(n.publish_time) if n.publish_time else None
        related_news.append(d)

    # 详情自己
    detail_dict = NewsDetailResponse.model_validate(news_orm).model_dump(by_alias=True)
    detail_dict["publishTime"] = str(news_orm.publish_time) if news_orm.publish_time else None
    detail_dict["views"] = news_orm.views + 1  # 浏览量 +1（increase_news_view 已经 update 了 DB）
    detail_dict["relatedNews"] = related_news  # 前端 NewsDetail.vue 读 relatedNews

    await set_json_cache(cache_key, detail_dict, expire_seconds=1800)
    return success_response(data=detail_dict)
