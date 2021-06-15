from app.services.admin.file import batchRemove, delete_photo_by_id, get_photo, upload_one
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager
from app.services.route_auth import authorize_and_log, authorize


templates = Jinja2Templates(directory="app/resources/templates")

router = APIRouter()

@router.get("/")
async def index(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:file:main", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/photo/photo.html", {"request": request, "authorize": authorize, "current_user": user})

#  图片数据
@router.get('/table')
async def gettable(page:int, limit: int, request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:file:main", user, request):
        return {"msg": "权限不足", "success": False}
    data, count = get_photo(page=page, limit=limit)
    res = {
        'msg': "",
        'code': 0,
        'data': data,
        'count': count,
        'limit': "10"

    }
    return res

@router.get("/upload")
async def upload(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:file:add", user, request):
        return {"msg": "权限不足", "success": False}
    return templates.TemplateResponse("admin/photo/photo_add.html", {"request": request})

# 图片上传
@router.post("/upload")
async def upload(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:file:add", user, request):
        return {"msg": "权限不足", "success": False}
    req = await request.form()
    photo = req.get("file")
    mime = req.get("file").content_type
    file_url = upload_one(photo=photo, mime=mime)
    res = {
            "msg": "上传成功",
            "code": 0,
            "data":
                {"src": file_url}
    }
    return res


# 图片删除
@router.post('/delete')
async def delete(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:file:delete", user, request):
        return {"msg": "权限不足", "success": False}
    id = (await request.form()).get('id')
    res = delete_photo_by_id(id)
    if res:
        return {"msg": "删除成功", "code": 200}
    else:
        return {"msg": "删除失败", "code": 999}

# 图片删除
@router.post('/batchRemove')
async def delete(request: Request, user=Depends(manager)):
    if not authorize_and_log("admin:file:delete", user, request):
        return {"msg": "权限不足", "success": False}
    ids = (await request.form()).getlist('ids[]')
    res = batchRemove(ids)
    if res:
        return {"msg": "删除成功", "code": 200}
    else:
        return {"msg": "删除失败", "code": 999}