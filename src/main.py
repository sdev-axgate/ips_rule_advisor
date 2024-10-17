# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.auth.auth_routes import router as auth_router
from src.openai.openai_routes import router as openai_router
from src.root.root import router as root_router
from src.getinfo.getinfo_routes import router as getinfo_router
from src.login.login import router as login_router
from src.ruletest.ruletest_router import router as ruletest_router
from src.rule.rule import router as rule_router
from src.finalreport.finalreport_routes import router as final_router
from src.mypage.mypage_routes import router as mypage_router
from src.settings.settings_routes import router as settings_router
from src.sidebar.sidebar_route import router as sidebar_router
import uvicorn
import asyncio
from src.getinfo import rpatools

app = FastAPI()

# 프로그램 시작 시 동작하게 하기
# 1초마다, 대기열에 있는 아직 수행 안된 테스트를, 현재 사용 가능한 테스트 서버에 보내기
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(rpatools.do_remainning_test())


# Static files setup
app.mount("/static", StaticFiles(directory="./src/static"), name="static")
app.mount("/profile", StaticFiles(directory="profile"), name="profile")

# Include routers
app.include_router(auth_router, prefix="/auth")
app.include_router(openai_router, prefix="/openai", tags=["openai"])
app.include_router(ruletest_router, prefix="/rule")
app.include_router(root_router)
app.include_router(getinfo_router)
app.include_router(login_router)
app.include_router(rule_router)
app.include_router(final_router)
app.include_router(mypage_router)
app.include_router(settings_router)
app.include_router(sidebar_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
