from sqlalchemy import select, func, delete

from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News


async def add_favorite(db: AsyncSession, user_id: int, news_id: int):
    """收藏一条新闻，已经收藏过就返回 None"""
    existing = await db.execute(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    )
    if existing.scalar_one_or_none():
        return None

    fav = Favorite(user_id=user_id, news_id=news_id)
    db.add(fav)
    await db.commit()
    await db.refresh(fav)
    return fav


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    """取消收藏某条新闻，返回是否真的删掉了"""
    stmt = delete(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_user_favorites(db: AsyncSession, user_id: int):
    """清空当前用户的全部收藏，返回删掉的条数"""
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


async def get_user_favorites(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    """
    联表查收藏记录 + 新闻详情
    返回 [(收藏记录, 新闻), ...]，具体怎么拼成响应交给上层 schemas/routers 处理
    """
    stmt = (
        select(Favorite, News)
        .join(News, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [(row[0], row[1]) for row in rows]


async def get_user_favorites_count(db: AsyncSession, user_id: int):
    stmt = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def is_favorited(db: AsyncSession, user_id: int, news_id: int):
    stmt = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None
