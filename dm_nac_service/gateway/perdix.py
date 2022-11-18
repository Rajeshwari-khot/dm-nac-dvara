import requests
from fastapi import APIRouter
from datetime import datetime
from fastapi.responses import JSONResponse
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.resource.generics as generics
from dm_nac_service.schemas.logs import LogBase
from dm_nac_service.resource.exceptions import _raiseException
import dm_nac_service.repository.logs as logs
from dm_nac_service.commons import get_env_or_fail


router = APIRouter()
PERDIX_SERVER = 'perdix-server'
validate_url = get_env_or_fail(PERDIX_SERVER, 'perdix-base-url', PERDIX_SERVER + ' base-url not configured')
NAC_SERVER='nac-server'


async def perdix_post_login():
    """ Generic Post Method for perdix login """
    try:        
        username = get_env_or_fail(PERDIX_SERVER, 'username', PERDIX_SERVER + ' username not configured')
        password = get_env_or_fail(PERDIX_SERVER, 'password', PERDIX_SERVER + ' password not configured')
        url = validate_url + f'/oauth/token?client_id=application&client_secret=mySecretOAuthSecret&grant_type=password&password={password}&scope=read+write&skip_relogin=yes&username={username}'
        str_url = str(url)
        login_context_response = requests.post(url)
        login_context_dict = generics.response_to_dict(login_context_response)
        api_call_duration = str(login_context_response.elapsed.total_seconds()) + ' sec'
        log_info = LogBase(
            channel='Perdix',
            request_url=str_url,
            request_method='POST',
            params=f"username={username} password={password}",
            request_body="",
            response_body=str(login_context_dict),
            status_code=str(login_context_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await logs.insert(log_info)
        return login_context_response
    except Exception as e:
        logger.exception(f"GATEWAY - PERDIX - PERDIX POST LOGIN - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
           
        
async def perdix_fetch_loan(loan_id):
    """ Generic Post Method for perdix fetch customer """
    try:
        url = validate_url + f'/api/individualLoan/{loan_id}'
        str_url = str(url)
        login_token = await perdix_post_login()
        login_token_dict=generics.response_bytes_to_dict(login_token)
        access_token=login_token_dict.get('access_token')
        headers = {
                "Content-Type": "application/json",
                "Content-Length": "0",
                "User-Agent": 'My User Agent 1.0',
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Authorization": f"bearer {access_token}"
            }
        loan_context_response = requests.get(url, headers=headers)  
        loan_context_response_dict=generics.response_bytes_to_dict(loan_context_response)
        str_data = str(loan_context_response_dict)
        api_call_duration = str(loan_context_response.elapsed.total_seconds()) + ' sec'
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='Perdix',
            request_url=str_url,
            request_method='GET',
            params=f"token={login_token}",
            request_body="",
            response_body=str(info),
            status_code=str(loan_context_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        log_id = await logs.insert(log_info)
        return loan_context_response
    except Exception as e:
        logger.exception(f"GATEWAY - PERDIX - PERDIX FETCH LOAN - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
            
    
async def perdix_update_loan(loan_data):
    """ Generic put Method to update perdix customer """
    try:
        url = validate_url + f'/api/individualLoan'
        str_url = str(url)
        login_token = await perdix_post_login()
        login_token_dict=generics.response_bytes_to_dict(login_token)
        access_token=login_token_dict.get('access_token')
        headers = {
                "Content-Type": "application/json",
                "Content-Length": "0",
                "User-Agent": 'My User Agent 1.0',
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Authorization": f"bearer {access_token}"
            }
        str_url = str(url)
        loan_update_response = requests.put(url, json=loan_data, headers=headers)
        loan_update_response_dict = generics.response_bytes_to_dict(loan_update_response)
        api_call_duration = str(loan_update_response.elapsed.total_seconds()) + ' sec'
        str_data=str(loan_update_response_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data 
        log_info = LogBase(
        channel='Perdix',
        request_url=str_url,
        request_method='PUT',
        params="",
        request_body="",
        response_body=str(info),
        status_code=str(loan_update_response.status_code),
        api_call_duration=api_call_duration,
        request_time=str(datetime.now())
        )
        await logs.insert(log_info)
        return loan_update_response
    except Exception as e:
        logger.exception(f"GATEWAY - PERDIX - PERDIX UPDATE LOAN - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
            
        


