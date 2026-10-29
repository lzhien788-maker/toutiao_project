from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteAddRequest, FavoriteItemResponse
from utils.author import get_current_user
from utils.response import success_response, error_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.post("/add")
async def collect_news(
    body: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    fav = await favorite.add_favorite(db, user.id, body.news_id)
    if fav is None:
        return error_response(code=400, message="已经收藏过了")
    return success_response(message="收藏成功", data={"favoriteId": fav.id})


# 前端用的是 DELETE /api/favorite/remove?newsId=xxx，这里两个路径都注册一份
@router.delete("/remove")
@router.delete("")
async def cancel_collect(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ok = await favorite.remove_favorite(db, user.id, news_id)
    if not ok:
        return error_response(code=404, message="没有收藏过这条新闻")
    return success_response(message="取消收藏成功")


@router.delete("/clear")
async def clear_collects(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """清空当前用户的全部收藏"""
    count = await favorite.clear_user_favorites(db, user.id)
    return success_response(message="清空收藏成功", data={"count": count})


@router.get("/list")
async def list_collects(
    page: int = 1,
    page_size: int = Query(10, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    收藏列表。
    前端 Favorite.vue 用的是扁平结构（item.id / item.title / item.publishTime / item.favoriteTime），
    所以这里把「收藏记录」和「新闻」拼成一条扁平数据返回。
    """
    offset = (page - 1) * page_size
    rows = await favorite.get_user_favorites(db, user.id, offset, page_size)
    total = await favorite.get_user_favorites_count(db, user.id)
    has_more = (offset + len(rows)) < total

    items = []
    for fav, news in rows:
        items.append(
            FavoriteItemResponse(
                id=news.id,  # ★ 用新闻ID，前端要拿它跳转详情 / 取消收藏
                title=news.title,
                image=news.image,
                description=news.description,
                publish_time=str(news.publish_time) if news.publish_time else None,
                author=news.author,
                views=news.views,
                favorite_time=str(fav.created_at) if fav.created_at else None,
            ).model_dump(by_alias=True)
        )

    return success_response(
        message="获取收藏列表成功",
        data={"list": items, "total": total, "hasMore": has_more},
    )


@router.get("/check")
async def check_collect(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """前端 store/modules/favorite.js 读的是 data.isFavorite"""
    favorited = await favorite.is_favorited(db, user.id, news_id)
    return success_response(data={"isFavorite": favorited})
