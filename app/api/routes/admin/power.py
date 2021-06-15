from app.services.power import batch_remove, disable_status, enable_status, get_power_by_id, get_power_dict, remove_power, save_power, select_parent, update_power
from fastapi_sqlalchemy import db
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager
from fastapi import APIRouter, Request, Depends
from app.services.route_auth import authorize_and_log, authorize

templates = Jinja2Templates(directory="app/resources/templates")


router = APIRouter()

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:main", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/power/main.html", {"request": request, "authorize": authorize, "current_user": user})



@router.get("/data")
async def data(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:main", user, request):
        return {"msg": "权限不足", "success": False}
    power_data = get_power_dict()
    res = {
        "data": power_data
    }
    return res

# 增加
@router.get("/add")
async def add(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:add", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/power/add.html", {"request": request})


@router.get('/selectParent')
def selectParent(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:add", user, request):
        return {"msg": "权限不足", "success": False}
    power_data = select_parent()
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": power_data

    }
    return res

# 增加
@router.post("/save")
async def save(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:add", user, request):
        return {"msg": "权限不足", "success": False}
    req = await request.json()
    save_power(req)
    return {"msg": "成功", "success": True}

# 权限编辑
@router.get('/edit/{id}')
async def edit(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:edit", user, request):
        return {"msg": "权限不足", "success": False}
    power = get_power_by_id(id)
    icon = str(power.icon).split()
    if len(icon) == 2:
        icon = icon[1]
    else:
        icon = None
    return templates.TemplateResponse("admin/power/edit.html", {"request": request, "power": power, "icon": icon})

# 权限角色
@router.put('/update')
async def update(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:edit", user, request):
        return {"msg": "权限不足", "success": False}
    res = await request.json()
    r = update_power(res)
    if not r:
        return {"msg": "更新权限失败", "success": False}
    return {"msg": "更新权限成功", "success": True}


# 启用权限
@router.put('/enable')
async def enable(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:edit", user, request):
        return {"msg": "权限不足", "success": False}
    id = dict(await request.json()).get('powerId')
    if id:
        res = enable_status(id)
        if not res:
            return {"msg": "出错啦", "success": False}
        return {"msg": "启动成功", "success": True}
    return {"msg": "数据错误", "success": False}

# 禁用权限
@router.put('/disable')
async def disenable(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:edit", user, request):
        return {"msg": "权限不足", "success": False}
    id = dict(await request.json()).get('powerId')
    if id:
        res = disable_status(id)
        if not res:
            return {"msg": "出错啦", "success": False}
        return {"msg": "禁用成功", "success": True}
    return {"msg": "数据错误", "success": False}

# 角色删除
@router.delete('/remove/{id}')
async def remove(id: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:remove", user, request):
        return {"msg": "权限不足", "success": False}
    res = remove_power(id)
    if not res:
        return {"msg": "删除失败", "success": False}
    return {"msg": "删除成功", "success": True}

# 批量删除
@router.delete('/batchRemove')
async def remove(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:power:remove", user, request):
        return {"msg": "权限不足", "success": False}
    ids = (await request.form()).getlist("ids[]")
    batch_remove(ids)
    return {"msg": "批量删除成功", "success": True}