from app.models.admin import Role
from app.services.user import add_user, add_user_role, batch_remove, delete_by_id, enable_status, get_user_by_id, get_user_by_name, get_user_data_dict, is_user_exists, update_user, update_user_role, disable_status
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager
from fastapi_sqlalchemy import db
from app.services.route_auth import authorize_and_log, authorize


templates = Jinja2Templates(directory="app/resources/templates")


router = APIRouter()

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:main", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/user/main.html", {"request": request, "authorize": authorize, "current_user": user})

# 表格数据
@router.get("/data")
async def getData(request: Request, page: int, limit: int, realName: str=None, username: str=None, user=Depends(manager)):
    if not authorize_and_log("admin:user:main", user, request):
        return {"msg": "权限不足", "success": False}
    filters = {}
    if realName:
        filters["realname"] = ('%' + realName + '%')
    if username:
        filters["username"] = ('%' + username + '%')
    data, count = get_user_data_dict(page=page, limit=limit, filters=filters)
    res = {
        'msg': "",
        'code': 0,
        'data': data,
        'count': count,
        'limit': "10"

    }
    return res

# 增加
@router.get("/add")
async def add(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:add", user, request):
        return {"msg": "权限不足", "success": False}
    roles = db.session.query(Role).all()
    return templates.TemplateResponse("admin/user/add.html", {"request": request, "roles": roles})

# 增加
@router.post("/save")
async def save(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:add", user, request):
        return {"msg": "权限不足", "success": False}
    req = dict(await request.json())
    a = req.get("roleIds")
    username = req.get('username')
    realName = req.get('realName')
    password = req.get('password')
    role_ids = a.split(',')
    if not username or not realName or not password:
        return {"msg": "账号姓名密码不得为空", "success": False}

    if is_user_exists(username):
        return {"msg": "用户已经存在", "success": False}
    id = add_user(username, realName, password)
    add_user_role(id, role_ids)
    return {"msg": "增加成功", "success": True}

# 编辑
@router.get('/edit/{id}')
async def edit(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:edit", user, request):
        return {"msg": "权限不足", "success": False}
    user = get_user_by_id(id)
    roles = db.session.query(Role).all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return templates.TemplateResponse("admin/user/edit.html", {"request": request, "user": user, "roles": roles, "checked_roles": checked_roles})

# 角色
@router.put('/update')
async def update(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:edit", user, request):
        return {"msg": "权限不足", "success": False}
    res = dict(await request.json())
    a = res.get("roleIds")
    id = res.get("userId")
    username = res.get('username')
    realName = res.get('realName')
    role_ids = a.split(',')
    update_user(id, username, realName)
    update_user_role(id, role_ids)
    return {"msg": "更新成功", "success": True}


# 启用用户
@router.put('/enable')
async def enable(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:edit", user, request):
        return {"msg": "权限不足", "success": False}
    id = dict(await request.json()).get('userId')
    if id:
        res = enable_status(id)
        if not res:
            return {"msg": "出错啦", "success": False}
        return {"msg": "启动成功", "success": True}
    return {"msg": "数据错误", "success": False}

# 禁用用户
@router.put('/disable')
async def disenable(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:edit", user, request):
        return {"msg": "权限不足", "success": False}
    id = dict(await request.json()).get('userId')
    if id:
        res = disable_status(id)
        if not res:
            return {"msg": "出错啦", "success": False}
        return {"msg": "禁用成功", "success": True}
    return {"msg": "数据错误", "success": False}

# 用户删除
@router.delete('/remove/{id}')
async def remove(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:remove", user, request):
        return {"msg": "权限不足", "success": False}
    res = delete_by_id(id)
    if not res:
        return {"msg": "删除失败", "success": False}
    return {"msg": "删除成功", "success": True}

# 批量删除
@router.delete('/batchRemove')
async def remove(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:user:remove", user, request):
        return {"msg": "权限不足", "success": False}
    ids = (await request.form()).getlist("ids[]")
    batch_remove(ids)
    return {"msg": "批量删除成功", "success": True}