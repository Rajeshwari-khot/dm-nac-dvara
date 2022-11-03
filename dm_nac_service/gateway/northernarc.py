from datetime import datetime
import json
import requests

from fastapi.responses import JSONResponse

# data
from dm_nac_service.schemas.logs import LogBase
# repository
import dm_nac_service.repository.logs as api_logs
from dm_nac_service.utils import get_env_or_fail
import dm_nac_service.resource.generics as generics
import dm_nac_service.app_responses.disbursement as disbursement_response

from dm_nac_service.resource.logging_config import logger

NAC_SERVER = 'northernarc-server'
validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
sector_id = get_env_or_fail(NAC_SERVER, 'sector-id', NAC_SERVER + 'Sector ID not configured')

async def nac_dedupe(context, data):
    """Generic Post Method for dedupe"""
    """get data from perdix and post into dedupe endpoint"""
    try:
        
        url = validate_url + f'/{context}?originatorId={originator_id}&sectorId={sector_id}'
        str_url = str(url)
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
        print("get_root",get_root)
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



async def nac_disbursement(context, data):
    """Generic Post Method for disbursment"""
    """get data from perdix and post into disbursment endpoint"""
    try:
        
        url = validate_url + f'/po/{context}/request'
        str_url = str(url)
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
        
        disbursement_context_response = requests.post(url, json=data, headers=headers)
        #fake success response 1
        disbursement_context_dict = disbursement_response.disbursement_request_success_response
        # disbursement_context_dict = disbursement_response.disbursement_request_error_response1
        # disbursement_context_dict = disbursement_response.disbursement_request_error_response2
        # disbursement_context_dict = disbursement_response.disbursement_request_error_response3
        
        api_call_duration = str(disbursement_context_response.elapsed.total_seconds()) + ' sec'
        str_data = str(disbursement_context_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='NorthernArc',
            request_url=url,
            request_method='POST',
            params="",
            request_body=str(data),
            response_body=str(info),
            status_code=str(disbursement_context_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return disbursement_context_dict
    except Exception as e:
        logger.exception(f"GATEWAY - NORTHERNARC - NAC DISBURSEMENT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def get_disbursement_status(context, disbursement_reference_id):
    """Generic GET Method for Disbursement"""
    """send disburement_ref_id to disbursement status check endpoint"""
    try:
        
        url = validate_url + f'/po/{context}/status/originatorId={originator_id}&disbursementReferenceId={disbursement_reference_id}'
        str_url = str(url)
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
        disbursement_status_response = requests.get(url, headers=headers )
        # disbursement_status_response_dict = generics.response_to_dict(disbursement_status_response)

        # Fake Success Response1 to test PENNY_DROP AND IN_PROGRESS
        disbursement_status_response_dict = disbursement_response.disbursement_status_success_response1

        # Fake Success Response2 to test with UTR
        # disbursement_status_response_dict = disbursement_response.disbursement_status_success_response2

        # Fake Error Response1 to test INVALID DISBURSEMENT ID status and message
        # disbursement_status_response_dict = disbursement_status_error_response1

        # Fake Error Response2 to test PENNY_DROP AND FAILED
        # disbursement_status_response_dict = disbursement_status_error_response2

        # Fake Error Response3 to test AMOUNT_DISBURSEMENT AND FAILED
        # disbursement_status_response_dict = disbursement_status_error_response3

        api_call_duration = str(disbursement_status_response.elapsed.total_seconds()) + ' sec'
        str_data = str(disbursement_status_response_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='NorthernArc',
            request_url=url,
            request_method='POST',
            params="",
            request_body=str(str_data),
            response_body=str(info),
            status_code=str(disbursement_status_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return disbursement_status_response_dict
    except Exception as e:
        logger.exception(f"GATEWAY - NORTHERNARC - NAC DISBURSEMENT STATUS- {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


async def nac_sanction(data):
    """ Generic Post Method for sanction """
    """get data from perdix and post into northern_arc sanction endpoint"""
    try:
        
        url = validate_url + f'/po/uploadSanctionJSON?originatorId={originator_id}&sectorId={sector_id}'
        str_url = str(url)
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
        print(sanction_context_response.status_code,sanction_context_response.content)
        sanction_context_response_dict = generics.response_to_dict(sanction_context_response)
        print(sanction_context_response_dict)
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
        logger.exception(f"GATEWAY -  - CREATE SANCTION - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
