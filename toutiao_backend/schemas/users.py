from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str


class UserInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    avatar: str | None = None
    bio: str | None = None


class UserAuthResponse(BaseModel):
    """
    登录 / 注册成功后的返回体。
    前端 store/user.js 读的是 response.data.data.userInfo，
    所以用 serialization_alias 把 user_info 序列化成 userInfo。
    """
    model_config = ConfigDict(populate_by_name=True)

    token: str
    user_info: UserInfoResponse = Field(serialization_alias="userInfo")


class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None


class UserPasswordUpdateRequest(BaseModel):
    """
    前端提交的是 { oldPassword, newPassword }，
    用 alias 兼容驼峰写法，populate_by_name 让下划线写法也能用。
    """
    model_config = ConfigDict(populate_by_name=True)

    old_password: str = Field(alias="oldPassword")
    new_password: str = Field(alias="newPassword")
