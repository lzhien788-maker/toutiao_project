"""
Redis 缓存配置
视频第2步：配置 Redis 客户端
"""
from redis.asyncio import Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import (
    ConnectionError,
    TimeoutError,
)

# ========== Redis 连接配置 ==========
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None  # 如果 Redis 设了密码，填这里

# ========== 创建异步 Redis 客户端 ==========
# retry=Retry(ExponentialBackoff(), 3) 表示连接失败时最多重试 3 次，指数退避
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,          # 自动把 bytes 解码成 str
    retry=Retry(ExponentialBackoff(), 3),
)


async def test_redis_connection():
    """启动时测试 Redis 是否能连上（可在 main.py startup 里调用）"""
    try:
        await redis_client.ping()
        print("✅ Redis 连接成功")
        return True
    except (ConnectionError, TimeoutError) as e:
        print(f"❌ Redis 连接失败: {e}")
        print("请先启动 Redis 服务：Windows 下执行 redis-server.exe")
        return False
