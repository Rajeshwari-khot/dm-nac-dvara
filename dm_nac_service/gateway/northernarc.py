import json
import requests
import os
from datetime import datetime
import shutil
import urllib.request
import shlex
import subprocess
from fastapi.responses import JSONResponse
from dm_nac_service.schemas.logs import LogBase
import dm_nac_service.repository.logs as api_logs
from dm_nac_service.utils import get_env_or_fail
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.resource.generics as generics

NAC_SERVER = 'northernarc-server'
PERDIX_SERVER='perdix-server'
validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
sector_id = get_env_or_fail(NAC_SERVER, 'sector-id', NAC_SERVER + 'Sector ID not configured')

async def nac_dedupe(data):
    """Generic Post Method for dedupe"""
    """get data from perdix and post into dedupe endpoint"""
    try:       
        url = validate_url + f'/dedupe?originatorId={originator_id}&sectorId={sector_id}'
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        # Data Prepared using automator Data
        get_root =[data]    
        dedupe_context_response = requests.post(url, json=get_root, headers=headers)        
        response_content = dedupe_context_response.content
        dedupe_context_dict = json.loads(response_content.decode('utf-8'))        
        api_call_duration = str(dedupe_context_response.elapsed.total_seconds()) + ' sec'
        str_data = str(dedupe_context_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='NorthernArc',
            request_url=url,
            request_method='POST',
            params=f"originatorId={originator_id},sectorId={sector_id}",
            request_body=str(data),
            response_body=str(info),
            status_code=str(dedupe_context_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return dedupe_context_response
    except Exception as e:
        logger.exception(f"GATEWAY - NORTHERNARC - NAC DEDUPE - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def nac_sanction(data):
    """ Generic Post Method for sanction """
    """get data from perdix and post into northern_arc sanction endpoint"""
    try:        
        url = validate_url + f'/po/uploadSanctionJSON?originatorId={originator_id}&sectorId={sector_id}'
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        sanction_context_response = requests.post(url, json=data, headers=headers)   
        sanction_context_response_dict = generics.response_to_dict(sanction_context_response)       
        api_call_duration = str(sanction_context_response.elapsed.total_seconds()) + ' sec'
        str_data = str(sanction_context_response_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='northernarc',
            request_url=url,
            request_method='POST',
            params=f"{originator_id},{sector_id}",
            request_body=str(data),
            response_body=str(info),
            status_code=str(sanction_context_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return sanction_context_response
    except Exception as e:
        logger.exception(f"GATEWAY - sanction - CREATE SANCTION - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


async def nac_file_upload(customer_id, file, file_type):
    try:       
        file_stream_url = get_env_or_fail(PERDIX_SERVER, 'perdix-stream-url', PERDIX_SERVER + 'Stream URL is not configured')
        url = validate_url + f'/po/uploadFile?originatorId={originator_id}&fileType={file_type}&customerId={customer_id}'
        payload={}
        image_id = '94d150e4-6232-4f5e-a341-494d76c5c4bf'
        tmp_file = "./static/" + image_id
        file_url = file_stream_url + image_id
        headers = {
            "Accept":"*/*",
            "GROUP-KEY": group_key,
            "API-KEY": api_key,
            "Content-Type":"multipart/form-data;" 
        }
        urllib.request.urlretrieve(file_url, tmp_file)
        file_name = file.filename
        file_path = os.path.abspath(('./static/'))       
        with open('test', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            shutil.copyfile('test', file_path + '/' + file_name)
        if not os.path.exists(file_path + 'test'):
            os.remove(file_path + '/' + 'test')
            shutil.move('test', file_path)
        else:
            shutil.move('test', file_path)
        with open(file_path + '/' + file_name,"rb") as a_file:
            path_proper =  a_file.name      
        file_full_path = file_path+'/'+file_name
        cmd = f"""curl --location --request POST 'https://stage.northernarc.com/nimbus-services/api/po/uploadFile?originatorId={originator_id}&fileType={file_type}&customerId={customer_id}' --header 'accept: */*' --header 'GROUP-KEY: {group_key}' --header 'API-KEY: {api_key}' --form 'file=@{file_full_path}'"""
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()     
        file_response_context_dict = json.loads(stdout.decode('utf-8'))
        str_data=str(file_response_context_dict)       
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='northernarc',
            request_url=url,
            request_method='POST',
            params=f"{originator_id},{sector_id}",
            request_body="",
            response_body=str(info),
            status_code="file_upload_response.status_code",
            api_call_duration="",
            request_time=str(datetime.now()))
        await api_logs.insert(log_info)         
        result=file_response_context_dict
    except Exception as e:
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at Northern Arc Post Method - {e.args[0]}"})
        logger.exception(f" -Issue with file_upload_document function, {e.args[0]}")
    return result
   

async def get_nac_sanction(customer_id):
    """ Generic Post Method for sanction """
    """get data from perdix and post into northern_arc sanction endpoint"""
    try:  
        url = validate_url + f'/po/status?customerId={customer_id}&originatorId={originator_id}'       
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }   
        sanction_get_response = requests.get(url, headers=headers)           
        sanction_get_response_dict = generics.response_to_dict(sanction_get_response)     
        api_call_duration = str(sanction_get_response.elapsed.total_seconds()) + ' sec'
        str_data = str(sanction_get_response_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='northernarc',
            request_url=url,
            request_method='GET',
            params=f"{originator_id},{customer_id}",
            request_body="",
            response_body=str(info),
            status_code=str(sanction_get_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return sanction_get_response
    except Exception as e:
        logger.exception(f"GATEWAY - NAC - GET SANCTION-STATUS - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})   



