import traceback

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

DEBUG_MODE = True


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig)
    if "Duplicate entry" in error_msg:
        message = "数据重复，请检查唯一性字段"
    elif "foreign key" in error_msg.lower():
        message = "关联数据不存在，操作被拒绝"
    else:
        message = "数据库完整性约束错误"

    if DEBUG_MODE:
        message = f"{message}: {error_msg}"

    return JSONResponse(
        status_code=400,
        content={
            "code": 400,
            "message": message,
            "data": None,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_error = errors[0] if errors else {}
    field = ".".join(str(p) for p in first_error.get("loc", ()))
    msg = first_error.get("msg", "参数校验失败")
    message = f"{field}: {msg}" if field else msg

    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": message,
            "data": None,
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    if DEBUG_MODE:
        traceback.print_exc()
        message = str(exc) or "Internal Server Error"
    else:
        message = "服务器内部错误，请稍后重试"

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": message,
            "data": None,
        },
    )
