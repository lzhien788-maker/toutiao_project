from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from routers import favorite, news, users, history
from config.cache_config import test_redis_connection
from utils.exception import (
    global_exception_handler,
    http_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)

SWAGGER_JS_URL = "https://registry.npmmirror.com/swagger-ui-dist/5.34.0/files/swagger-ui-bundle.js"
SWAGGER_CSS_URL = "https://registry.npmmirror.com/swagger-ui-dist/5.34.0/files/swagger-ui.css"
REDOC_JS_URL = "https://registry.npmmirror.com/redoc/2.1.4/files/bundles/redoc.standalone.js"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时自动检测 Redis 是否可用"""
    print("\n===== 头条后端启动 =====")
    await test_redis_connection()
    print("========================\n")
    yield


app = FastAPI(
    title="头条后端",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
async def root():
    return {"messages": "hello World"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_js_url=SWAGGER_JS_URL,
        swagger_css_url=SWAGGER_CSS_URL,
    )


@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=app.title + " - ReDoc",
        redoc_js_url=REDOC_JS_URL,
    )


app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
