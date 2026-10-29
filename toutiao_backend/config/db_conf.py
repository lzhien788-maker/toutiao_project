from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import func, DateTime
from datetime import datetime

# ========== 数据库连接配置 ==========
# 注意：账号密码、数据库名 news_app 改成你自己的！
ASYNC_DATABASE_URL = "mysql+aiomysql://root:root@localhost:3306/news_app?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,        # 可选：打印执行的SQL语句，调试用，上线关掉
    pool_size=10,     # 连接池常驻连接
    max_overflow=20   # 额外临时连接上限
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ========== 基础模型基类 ==========
class Base(DeclarativeBase):
    create_time: datetime = func.now()
    update_time: datetime = func.now()

# ========== 获取数据库会话的依赖项 get_db ==========
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

