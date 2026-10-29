from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(message: str = "success", data: Any = None):
    content = {
        "code": 200,
        "message": message,
        "data": data,
    }
    return JSONResponse(content=jsonable_encoder(content))


def error_response(code: int = 500, message: str = "Internal Server Error", data: Any = None):
    content = {
        "code": code,
        "message": message,
        "data": data,
    }
    return JSONResponse(content=jsonable_encoder(content), status_code=code)