from fastapi import APIRouter


router = APIRouter()

from app.api.routes.index import index
from app.api.routes.admin import admin


router = APIRouter()

router.include_router(index.router, tags=["index"])
router.include_router(admin.router, tags=["admin"], prefix="/admin")
