from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.api.depends.manager import manager


templates = Jinja2Templates(directory="app/resources/templates")


router = APIRouter()

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index/index.html", {"request": request})
