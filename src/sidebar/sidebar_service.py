from supabase import Client
from fastapi import HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from src.auth.auth_service import getuserinfo

async def get_past_cve_list(client: Client, request: Request, response: Response):
    # 사용자 정보 가져오기
    user_info = getuserinfo(client=client,response=response,request=request)
    if isinstance(user_info, RedirectResponse):
        return user_info
    user_id = user_info["user"].user.id
    
    # 해당 사용자의 CVE 리스트, 결과물의 id 값 가져오기
    response = client.table("info").select("id, cve").eq("user_id", user_id).execute()
    
    # 데이터가 없는 경우에 대한 처리
    if not response.data:
        return []
    
    return response.data

async def get_past_test_list(client: Client, request: Request, response: Response):
    # 사용자 정보 가져오기
    user_info = getuserinfo(client=client,response=response,request=request)
    if isinstance(user_info, RedirectResponse):
        return user_info
    user_id = user_info["user"].user.id
    
    # 해당 사용자의 테스트 리스트 가져오기
    response = client.table("test_result").select("id, cve").eq("user_id", user_id).execute()
    
    # 데이터가 없는 경우에 대한 처리
    if not response.data:
        return []
    
    return response.data

async def get_final_report_list(client: Client, request: Request, response: Response):
    # 사용자 정보 가져오기
    user_info = getuserinfo(client=client,response=response,request=request)
    if isinstance(user_info, RedirectResponse):
        return user_info
    user_id = user_info["user"].user.id
    
    # 해당 사용자의 테스트 리스트 가져오기
    response = client.table("final_report").select("id, cve").eq("user_id", user_id).execute()
    
    # 데이터가 없는 경우에 대한 처리
    if not response.data:
        return []
    
    return response.data