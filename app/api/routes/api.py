from fastapi import APIRouter


router = APIRouter()

from app.api.routes.index import index
from app.api.routes.admin import admin
from app.api.routes.admin import monitor
from app.api.routes.admin import admin_log
from app.api.routes.admin import role
from app.api.routes.admin import power
from app.api.routes.admin import user
from app.api.routes.admin import file


router = APIRouter()

router.include_router(index.router, tags=["index"])
router.include_router(admin.router, tags=["admin"], prefix="/admin")
router.include_router(monitor.router, tags=["admin:monitor"], prefix="/admin/monitor")
router.include_router(admin_log.router, tags=["admin:log"], prefix="/admin/log")
router.include_router(role.router, tags=["admin:role"], prefix="/admin/role")
router.include_router(power.router, tags=["admin:power"], prefix="/admin/power")
router.include_router(user.router, tags=["admin:user"], prefix="/admin/user")
router.include_router(file.router, tags=["admin:file"], prefix="/admin/file")
