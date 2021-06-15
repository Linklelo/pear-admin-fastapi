from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager
from app.api.depends.mem_session import mem_session
from app.services.admin.index import add_auth_session, get_captcha, make_menu_tree
from fastapi_sqlalchemy import db
from app.models.admin import User
from datetime import timedelta
from app.services.admin_log import login_log


templates = Jinja2Templates(directory="app/resources/templates")


router = APIRouter()

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    realname = user.realname
    return templates.TemplateResponse("admin/index.html", {"request": request, "realname": realname})

@router.post('/login')
async def login(request: Request, username: str=Form(None), password: str=Form(None), captcha: str=Form(None)):
    if not username or not password or not captcha:
        return {"code":0, "msg":"用户名或密码没有输入", "success":False}
    s_code = mem_session.pop(captcha, None)
    if captcha != s_code:
        return {"code":0, "msg":"验证码错误", "success":False}
    user = db.session.query(User).filter_by(username=username).first()
    if user is None:
        return {"code":0, "msg":"不存在的用户", "success":False}

    if user.enable == 0:
        return {"code":0, "msg":"用户被暂停使用", "success":False}

    if username == user.username and user.validate_password(password):
        login_log(request, username, uid=user.id, is_access=True)
        add_auth_session(user)
        access_token = manager.create_access_token(
            data=dict(sub=username),
            expires=timedelta(hours=1.0)
        )
        response = JSONResponse(content={"code":1, "msg":"登录成功", "success":True})
        manager.set_cookie(response, access_token)
        return response

    return {"code":0, "msg":"用户名或密码错误", "success":False}

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.get("/getCaptcha")
async def getCaptcha():
    resp, code = get_captcha()
    mem_session[code] = code
    return resp

# 控制台页面
@router.get('/welcome')
def welcome(request: Request, user=Depends(manager)):
    return templates.TemplateResponse('admin/console/console.html', {"request": request})


@router.get("/menu")
async def getMenu(user=Depends(manager)):
    menu = make_menu_tree(user)
    return menu

@router.post("/logout")
async def logout(user=Depends(manager)):
    response = JSONResponse(content={"msg":"注销成功","success":True})
    manager.set_cookie(response, "null")
    return response
