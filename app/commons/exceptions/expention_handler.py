# -*- coding: utf-8 -*- 
# @Time : 2022/7/21 07:14 
# @Author : junjie
# @File : expention_handler.py

from fastapi import Request
from app.commons.settings.config import HTTP_MSG_MAP
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.commons.responses.response_model import ResponseDto
from fastapi.responses import JSONResponse
from app.commons.exceptions.global_exception import BusinessException, AuthException, PermissionException
from app.commons.responses.response_code import CodeEnum
from loguru import logger


# 自定义http异常处理器
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    res = ResponseDto(code=CodeEnum.HTTP_ERROR.code, msg=HTTP_MSG_MAP.get(exc.status_code, exc.detail))
    return JSONResponse(content=res.model_dump())


# 请求参数校验异常处理器
async def body_validation_exception_handler(request: Request, err: RequestValidationError):
    message_list = []
    for error in err.errors():
        loc = error.get("loc") or []
        field = str(loc[-1]) if loc else "参数"
        msg = error.get("msg") or "非法"
        message_list.append(f"{field}{msg}")
    message = ",".join(message_list)
    res = ResponseDto(code=CodeEnum.PARAMS_ERROR.code, msg=f"请求参数非法!{message}")
    return JSONResponse(content=res.model_dump())

# 业务异常处理器
async def business_exception_handler(request: Request, exc: BusinessException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.model_dump())

# 权限异常处理器
async def role_exception_handler(request: Request, exc: PermissionException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.model_dump())

# 用户登录态异常处理处理器
async def auth_exception_handler(request: Request, exc: AuthException):
    res = ResponseDto(code=exc.code, msg=exc.msg)
    return JSONResponse(content=res.model_dump())

# todo 返回参数异常处理处理器
# async def res_validation_exception_handler(request: Request, exc: ValidationError):
#     res = ResponseDto(code=111, msg='demo')
#     return JSONResponse(content=res.dict())

# 全局系统异常处理器(中间件的异常都归类到这里来，统一处理)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, PermissionException):
        return await role_exception_handler(request, exc)
    elif isinstance(exc, AuthException):
        return await auth_exception_handler(request, exc)
    # elif isinstance(exc, ValidationError):
    #     return await res_validation_exception_handler(request, exc)
    else:
        import traceback
        logger.exception(traceback.format_exc())
        res = ResponseDto(code=CodeEnum.SYSTEM_ERROR.code, msg=CodeEnum.SYSTEM_ERROR.msg)
        return JSONResponse(content=res.model_dump())
