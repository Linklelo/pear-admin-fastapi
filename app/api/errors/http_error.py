from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/resources/templates")
    

async def http_error_handler(_: Request, exc: HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("errors/404.html", {"request": _}, status_code=exc.status_code)
    elif exc.status_code == 403:
        return templates.TemplateResponse("errors/403.html", {"request": _}, status_code=exc.status_code)
    elif exc.status_code == 500:
        return templates.TemplateResponse("errors/500.html", {"request": _}, status_code=exc.status_code)
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)