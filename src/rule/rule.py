from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@router.get("/redirect-to-home")
async def redirect_to_home():
    return RedirectResponse(url="/")

@router.get("/ruletest", response_class=HTMLResponse)
async def ruletest(request: Request):
    return templates.TemplateResponse("ruletest.html", {"request": request})

@router.get("/ruletest/result", response_class=HTMLResponse)
async def ruletest(request: Request,testid:str):
    return templates.TemplateResponse("ruletest_result.html", {"request": request, "testid": testid})

