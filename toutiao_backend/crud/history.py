from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_or_update_history(db: AsyncSession, user_id: int, news_id: int):
    """记录浏览历史（upsert）：同一用户看过这条新闻就更新浏览时间，否则新增"""
    existing = await db.execute(
        select(History).where(
            History.user_id == user_id, History.news_id == news_id
        )
    )
    record = existing.scalar_one_or_none()
    if record:
        record.view_time = func.now()
        await db.commit()
        await db.refresh(record)
        return record

    record = History(user_id=user_id, news_id=news_id)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_user_history(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    """
    分页查询当前用户的浏览记录，按浏览时间倒序，并关联出新闻信息
    返回 [(浏览记录, 新闻), ...]，响应格式交给上层 schemas/routers 处理
    """
    stmt = (
        select(History, News)
        .join(News, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [(row[0], row[1]) for row in rows]


async def get_user_history_count(db: AsyncSession, user_id: int):
    """统计当前用户的浏览记录总数（用于分页）"""
    stmt = select(func.count(History.id)).where(History.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def del_user_history(db: AsyncSession, user_id: int, news_id: int):
    """
    删除当前用户对某条新闻的浏览记录（按新闻ID删）
    前端 History.vue 拿到的 item.id 就是新闻ID，所以按 news_id 删
    """
    stmt = delete(History).where(
        History.news_id == news_id, History.user_id == user_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_user_history(db: AsyncSession, user_id: int):
    """清空当前用户的全部浏览记录，返回删掉的条数"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
