from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_conf import get_db
from crud import users


async def get_current_user(
        authorization: str = Header(None, alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
    """
    解析 Authorization 头拿当前登录用户。
    头可以写成 "Bearer xxx"，也可以直接写 token，前端两种都能用。
    没带头或者 token 无效，统一返回 401（前端拦截器据此跳登录页）。
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未提供令牌，请先登录")

    token = authorization.replace("Bearer", "").strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未提供令牌，请先登录")

    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或者已经过期的令牌")
    return user
