from app.services.admin.role import add_role, batch_remove, disable_status, enable_status, get_role_by_id, get_role_data_dict, get_role_power, remove_role, update_role, update_role_power
from app.models.admin import AdminLog
from fastapi import APIRouter, Request, Depends
from sqlalchemy import desc
from fastapi_sqlalchemy import db
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager
from marshmallow import fields, Schema
from app.services.route_auth import authorize_and_log, authorize


templates = Jinja2Templates(directory="app/resources/templates")


router = APIRouter()

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:main", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/role/main.html", {"request": request, "authorize": authorize, "current_user": user})

# 表格数据
@router.get("/data")
async def getData(page: int, limit: int, roleName: str=None, roleCode: str=None, user=Depends(manager)):
    filters = {}
    if roleName:
        filters["name"] = ('%' + roleName + '%')
    if roleCode:
        filters["code"] = ('%' + roleCode + '%')
    data, count = get_role_data_dict(page=page, limit=limit, filters=filters)
    res = {
        'msg': "",
        'code': 0,
        'data': data,
        'count': count,
        'limit': "10"

    }
    return res

# 角色增加
@router.get("/add")
async def add(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:main", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/role/add.html", {"request": request})

# 角色增加
@router.post("/save")
async def save(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:main", user, request):
        return {"msg": "权限不足", "success": False}
    req = await request.json()
    add_role(req)
    return {"msg": "成功", "success": True}

# 角色授权
@router.get('/power/{id}')
async def getPower(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:power", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/role/power.html", {"request": request, "id": id})

# 角色授权
@router.get('/getRolePower/{id}')
async def getRolePower(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:main", user, request):
        return {"msg": "权限不足", "success": False}
    powers = get_role_power(id)
    res = {
        "data": powers,
        "status": {"code": 200, "message": "默认"}
    }
    return res

# 保存角色权限
@router.put('/saveRolePower')
async def saveRolePower(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:edit", user, request):
        return {"msg": "权限不足", "success": False}
    req_form = await request.form()
    powerIds = req_form.get("powerIds")
    power_list = powerIds.split(',')
    roleId = req_form.get("roleId")
    update_role_power(id=roleId, power_list=power_list)
    return {"msg": "授权成功", "success": True}

# 角色编辑
@router.get('/edit/{id}')
async def edit(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:edit", user, request):
        return {"msg": "权限不足", "success": False}
    role = get_role_by_id(id)
    return templates.TemplateResponse("admin/role/edit.html", {"request": request, "role": role})

# 更新角色
@router.put('/update')
async def update(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:edit", user, request):
        return {"msg": "权限不足", "success": False}
    res = await request.json()
    r = update_role(res)
    if not r:
        return {"msg": "更新角色失败", "success": False}
    return {"msg": "更新角色成功", "success": True}

# 启用用户
@router.put('/enable')
async def enable(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:edit", user, request):
        return {"msg": "权限不足", "success": False}
    id = dict(await request.json()).get('roleId')
    if id:
        res = enable_status(id)
        if not res:
            return {"msg": "出错啦", "success": False}
        return {"msg": "启动成功", "success": True}
    return {"msg": "数据错误", "success": False}

# 禁用用户
@router.put('/disable')
async def disenable(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:edit", user, request):
        return {"msg": "权限不足", "success": False}
    id = dict(await request.json()).get('roleId')
    if id:
        res = disable_status(id)
        if not res:
            return {"msg": "出错啦", "success": False}
        return {"msg": "禁用成功", "success": True}
    return {"msg": "数据错误", "success": False}

# 角色删除
@router.delete('/remove/{id}')
async def remove(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:remove", user, request):
        return {"msg": "权限不足", "success": False}
    res = remove_role(id)
    if not res:
        return {"msg": "角色删除失败", "success": False}
    return {"msg": "角色删除成功", "success": True}

# 批量删除
@router.delete('/batchRemove')
async def remove(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:role:remove", user, request):
        return {"msg": "权限不足", "success": False}
    ids = (await request.form()).getlist("ids[]")
    batch_remove(ids)
    return {"msg": "批量删除成功", "success": True}