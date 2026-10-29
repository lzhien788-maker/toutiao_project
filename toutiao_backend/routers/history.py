from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest, HistoryItemResponse
from utils.author import get_current_user
from utils.response import success_response, error_response

router = APIRouter(prefix="/api/history", tags=["history"])


# 前端用的是 POST /api/history/add，这里两个路径都注册一份
@router.post("/add")
@router.post("")
async def record_history(
    body: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """记录一条浏览历史（幂等，重复浏览只刷新时间）"""
    await history.add_or_update_history(db, user.id, body.news_id)
    return success_response(
        message="记录浏览历史成功",
        data={"newsId": body.news_id},
    )


@router.get("/list")
async def list_history(
    page: int = 1,
    page_size: int = Query(10, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    分页查询当前用户的浏览历史。
    前端 History.vue 用的是扁平结构（item.id / item.title / item.publishTime / item.viewTime），
    所以这里把「浏览记录」和「新闻」拼成一条扁平数据返回。
    """
    offset = (page - 1) * page_size
    rows = await history.get_user_history(db, user.id, offset, page_size)
    total = await history.get_user_history_count(db, user.id)
    has_more = (offset + len(rows)) < total

    items = []
    for hist, news in rows:
        items.append(
            HistoryItemResponse(
                id=news.id,  # ★ 用新闻ID，前端要拿它跳转详情 / 删除这条记录
                title=news.title,
                image=news.image,
                description=news.description,
                publish_time=str(news.publish_time) if news.publish_time else None,
                author=news.author,
                views=news.views,
                view_time=str(hist.view_time) if hist.view_time else None,
            ).model_dump(by_alias=True)
        )

    return success_response(
        message="获取浏览历史成功",
        data={"list": items, "total": total, "hasMore": has_more},
    )


@router.delete("/delete/{news_id}")
async def delete_history(
    news_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除当前用户对某条新闻的浏览记录（路径参数是新闻ID）"""
    ok = await history.del_user_history(db, user.id, news_id)
    if not ok:
        return error_response(code=404, message="浏览记录不存在")
    return success_response(message="删除成功")


@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """清空当前用户的全部浏览记录"""
    count = await history.clear_user_history(db, user.id)
    return success_response(message="清空浏览历史成功", data={"count": count})
