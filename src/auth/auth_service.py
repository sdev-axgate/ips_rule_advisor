from supabase import Client
from fastapi import HTTPException, Response, Request
from fastapi.responses import RedirectResponse
from fastapi.responses import RedirectResponse,HTMLResponse
from pydantic import BaseModel
        

class SignInData(BaseModel):
    email: str
    password: str
class Register(BaseModel):
    email: str
    password: str
    confirm_password: str


def sign_up(client: Client, email: str, password: str): # 회원가입?
    try:
        client.auth.sign_up({"email": email, "password": password})
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <body>
        <script>
        window.onload = function() {
            var fragment = window.location.hash.substring(1); // '#' 제거
            if (fragment) {
                // 프래그먼트 값을 쿼리 매개변수로 변환하여 서버로 리다이렉트
                window.location.href = '/auth/callback?' + fragment;
            }
        };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

def sign_in(request:Request,client: Client, email: str, password: str,response: Response): # 로그인?
    try:
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        print(res)
        if res.user:
            response.set_cookie(key="user", value=res.user.id)
            return {"status": "success"}
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def sign_out(client: Client, response: Response):
    try:
        response.delete_cookie(key="user")
        client.auth.sign_out()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def sign_in_google(client: Client, response: Response):
    try:
        res = client.auth.sign_in_with_oauth(
        {
            "provider": "google",
            "options": {
	            "redirect_to": "127.0.0.1:8000/callback"
	        },
        }
    )
        return RedirectResponse(url=res.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def callback(client: Client, request: Request,response:Response):
    try:
        code = request.query_params.get("access_token")
        rcode = request.query_params.get("refresh_token")
        response.set_cookie(key="user", value=code)
        client.auth.set_session(code, rcode)
        return {"status": "success"}  #어디로 보낼지는 체크필요
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def profile(client: Client,request:Request):
    try:
        # 쿠키에서 세션 토큰 가져오기
        session_token_from_cookie = request.cookies.get("user")
        if not session_token_from_cookie:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # 세션 토큰을 사용하여 사용자 정보 가져오기
        user_info = client.auth.get_user(session_token_from_cookie)
        if user_info:
            return {"user": user_info}
        else:
            raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    