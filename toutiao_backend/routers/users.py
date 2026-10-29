from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from crud import users

from config.db_conf import get_db
from crud.users import get_user_by_username
from models.users import User
from schemas.users import UserRequest, UserInfoResponse, UserAuthResponse, UserUpdateRequest, UserPasswordUpdateRequest
from utils.author import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):

    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)

    # ★ 和登录返回同一种结构，前端 register() 里读 data.userInfo / data.token
    auth_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user),
    )
    return success_response(
        message="注册成功",
        data=auth_data.model_dump(by_alias=True),
    )


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户或密码错误")
    token = await users.create_token(db, user.id)

    # ★ model_dump(by_alias=True) 才会把 user_info 输出成前端要的 userInfo
    auth_data = UserAuthResponse(
        token=token,
        user_info=UserInfoResponse.model_validate(user),
    )
    return success_response(message="登录成功啦", data=auth_data.model_dump(by_alias=True))


@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    # 前端直接把 data 当成 userInfo 用（id/username/avatar/bio），字段名本身不是驼峰，无需别名
    return success_response(
        message="获取用户信息成功",
        data=UserInfoResponse.model_validate(user).model_dump(),
    )


@router.put("/update")
async def update_user_info(
        user_data: UserUpdateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user = await users.update_user(db, user.username, user_data)
    return success_response(
        message="更新用户信息成功",
        data=UserInfoResponse.model_validate(user).model_dump(),
    )


@router.put("/password")
async def change_password(
        password_data: UserPasswordUpdateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    await users.update_password(db, user, password_data.old_password, password_data.new_password)
    return success_response(message="修改密码成功")

