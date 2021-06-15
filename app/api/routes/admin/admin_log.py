from app.models.admin import AdminLog
from fastapi import APIRouter, Request, Depends
from sqlalchemy import desc
from fastapi_sqlalchemy import db
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager
from marshmallow import fields, Schema


templates = Jinja2Templates(directory="app/resources/templates")


router = APIRouter()

#                               ----------------------------------------------------------
#                               -------------------------  日志管理 --------------------------
#                               ----------------------------------------------------------

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("admin/admin_log/main.html", {"request": request})


class LogSchema(Schema):  # 序列化类
    id = fields.Integer()
    method = fields.Str()
    uid = fields.Str()
    url = fields.Str()
    desc = fields.Str()
    ip = fields.Str()
    user_agent = fields.Str()
    success = fields.Bool()
    create_time = fields.DateTime()

#                               ==========================================================
#                                                            登录日志
#                               ==========================================================

@router.get("/loginLog")
async def getLoginLog(page: int, limit: int, user=Depends(manager)):
    log =  db.session.query(AdminLog).filter_by(url = '/admin/login').order_by(desc(AdminLog.create_time)).offset(page-1).limit(limit).all()
    count = db.session.query(AdminLog).filter_by(url = '/admin/login').count()
    role_schema = LogSchema(many=True)
    output = role_schema.dump(log)
    res = {
        'msg': "",
        'code': 0,
        'data': output,
        'count': count,
        'limit': "10"

    }
    return res

#                               ==========================================================
#                                                            操作日志
#                               ==========================================================

@router.get("/operateLog")
async def getLoginLog(page: int, limit: int, user=Depends(manager)):
    log =  db.session.query(AdminLog).filter(AdminLog.url != '/admin/login').order_by(desc(AdminLog.create_time)).offset(page-1).limit(limit).all()
    count = db.session.query(AdminLog).filter(AdminLog.url != '/admin/login').count()
    role_schema = LogSchema(many=True)
    output = role_schema.dump(log)
    res = {
        'msg': "",
        'code': 0,
        'data': output,
        'count': count,
        'limit': "10"

    }
    return res