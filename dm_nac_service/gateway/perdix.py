
import json
import requests
from fastapi import Body,APIRouter
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import shutil

import requests
import json
from fastapi.encoders import jsonable_encoder

from datetime import datetime
from dm_nac_service.resource.log_config import logger
from dm_nac_service.resource.generics import response_to_dict, hanlde_response_body, hanlde_response_status
from dm_nac_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from dm_nac_service.schemas.logs import LogBase
import dm_nac_service.repository.logs as api_logs
# from dm_nac_service.data.database import insert_logs, insert_logs_all
from dm_nac_service.commons import get_env_or_fail




#service
import dm_nac_service.routes.dedupe as dedupe_route

# config
from dm_nac_service.utils import get_env_or_fail
# data
from dm_nac_service.schemas.logs import LogBase
# repository
import dm_nac_service.repository.logs as logs
# resource
from dm_nac_service.resource.exceptions import _raiseException
import dm_nac_service.resource.generics as generics
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.repository.logs as api_logs

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
        api_call_duration = str(login_context_response.elapsed.total_seconds()) + ' sec'
        login_context_dict = generics.response_to_dict(login_context_response)
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
        _raiseException('gateway-perdix', 'perdix_post_login', e.args[0])


async def perdix_fetch_loan(loan_id):
    """ Generic Post Method for perdix fetch customer """
    try:
        
        login_token = await perdix_post_login()
        
        
        if login_token.status_code!=200:
            return login_token

        login_token_dict = generics.response_to_dict(login_token)
        access_token = login_token_dict.get('access_token')
        url = validate_url + f'/api/individualLoan/{loan_id}'
       
        
        headers = {
            "Content-Type": "application/json",
            "Content-Length":"0",
            "User-Agent":'My User Agent 1.0',
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"keep-alive",
            "Authorization": f"bearer {access_token}"
        }
        str_url = str(url)
        loan_context_response = requests.get(url, headers=headers)
        # print("loan_context_response",loan_context_response.content)
       
        api_call_duration = str(loan_context_response.elapsed.total_seconds()) + ' sec'
        loan_context_dict = generics.response_bytes_to_dict(loan_context_response)
        
        str_data = str(loan_context_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='Perdix',
            request_url=str_url,
            request_method='GET',
            params=f"token={login_token}",
            request_body="",
            response_body=info,
            status_code=str(loan_context_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        log_id = await logs.insert(log_info)
        return loan_context_response
    except Exception as e:
        _raiseException('gateway-perdix', 'perdix_fetch_loan', e.args[0])


async def perdix_update_loan(loan_data):
    """ Generic put Method to update perdix customer """
    try:
        url = validate_url + f'/api/individualLoan'
        str_url = str(url)
        login_token = await perdix_post_login()
        login_token_decode = jsonable_encoder(login_token)
       
        response_body = login_token_decode.get('body')
        response_body_json = json.loads(response_body)

        fetch_loan_response_decode_status = login_token_decode.get('status_code')

        # If login is success
        if (fetch_loan_response_decode_status == 200):
            login_token = response_body_json.get('access_token')
            headers = {
                "Content-Type": "application/json",
                "Content-Length": "0",
                "User-Agent": 'My User Agent 1.0',
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Authorization": f"bearer {login_token}"
            }
            str_url = str(url)
           
            loan_update_response = requests.put(url, json=loan_data, headers=headers)
            loan_update_response_dict = generics.response_to_dict(loan_update_response)
            api_call_duration = str(loan_update_response.elapsed.total_seconds()) + ' sec'
            # If loan update success
            if(loan_update_response.status_code == 200):
                log_info = LogBase(
                channel='Perdix',
                request_url=str_url,
                request_method='PUT',
                params="",
                request_body="",
                response_body=str(loan_update_response_dict),
                status_code=str(loan_update_response.status_code),
                api_call_duration=api_call_duration,
                request_time=str(datetime.now())
        )
                await logs.insert(log_info)
                result = JSONResponse(status_code=200, content=loan_update_response_dict)
            else:
                log_info = LogBase(
                channel='Perdix',
                request_url=str_url,
                request_method='PUT',
                params="",
                request_body="",
                response_body=str(loan_update_response_dict),
                status_code=str(loan_update_response.status_code),
                api_call_duration=api_call_duration,
                request_time=str(datetime.now())
                )
                loan_update_unsuccess = {"error": 'Error from Perdix', "error_description": loan_update_response_dict}
                result = JSONResponse(status_code=500, content=loan_update_unsuccess)
        else:
            response_body = login_token_decode.get('body')
            response_body_json = json.loads(response_body)
            response_body_error = response_body_json.get('error')
            response_body_description = response_body_json.get('error_description')
            log_info = LogBase(
            channel='Perdix',
            request_url=str_url,
            request_method='PUT',
            params="",
            request_body="",
            response_body=str(response_body_description),
            status_code=str(response_body.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
            )
            login_unsuccess = {"error": response_body_error, "error_description": response_body_description}
            result = JSONResponse(status_code=500, content=login_unsuccess)
           

    except Exception as e:
        _raiseException('gateway-perdix', 'perdix_update_loan', e.args[0])
        
    return result



# async def post_disbursement_automator_data(
    
#     request_info: dict = Body(...),
# ):
#     """Function to prepare user data from perdix automator"""
#     """fetch customer_id & sanctionreference_id from find_customer_sanction"""
#     """post the data into create_disburement function and get response along with disbursement_id"""
#     try:
#         # database = get_database()
        
#         # Below is for data published manually
#         payload = request_info
#         # Customer Data
#         customer_data = payload["enrollmentDTO"]["customer"]
#         loan_data = payload["loanDTO"]["loanAccount"]

#         # Loan Data
#         sm_loan_id = loan_data.get("id")
#         bank_accounts_info = {}
#         if len(customer_data["customerBankAccounts"]) > 0:
#             bank_accounts_info = customer_data["customerBankAccounts"][0]
        
#         customer_sanction_response = await find_customer_sanction(sm_loan_id)
#         # customer_sanction_response_status = hanlde_response_status(customer_sanction_response)
#         # customer_sanction_response_body = hanlde_response_body(customer_sanction_response)
#         if(customer_sanction_response == 200):
#             # sanction_ref_id = customer_sanction_response_body.get('sanctionRefId')
#             # customer_id = customer_sanction_response_body.get('customerId')
            
            
#             originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
           
#             disbursement_info = {
#                 "originatorId": originator_id,
#                 "sanctionReferenceId": int(sanction_ref_id),
#                 "customerId": int(customer_id),
#                 "requestedAmount": loan_data.get("loanAmount"),
#                 "ifscCode": bank_accounts_info.get("ifscCode"),
#                 "branchName":  bank_accounts_info.get("customerBankBranchName"),
#                 "processingFees": loan_data.get("processingFeeInPaisa"),
#                 "insuranceAmount": loan_data.get("insuranceFee"),
#                 "disbursementDate": loan_data.get("loanDisbursementDate")
#             }
            
#             # Real Endpoint
#             nac_disbursement_response = await create_disbursement(disbursement_info)
            
#             nac_disbursement_response_status = hanlde_response_status(nac_disbursement_response)
#             nac_disbursement_response_body = hanlde_response_body(nac_disbursement_response)

#             if(nac_disbursement_response_status == 200):
#                 logger.info(f'2-Successfully posted disbursement data to nac endpoint, {nac_disbursement_response_body}')
#                 disbursement_message = nac_disbursement_response_body['content']['message']
#                 disbursement_reference_id = nac_disbursement_response_body['content']['value']['disbursementReferenceId']
#                 payload['partnerHandoffIntegration']['status'] = 'SUCCESS'
#                 payload['partnerHandoffIntegration']['partnerReferenceKey'] = disbursement_reference_id
#                 update_loan_info = await update_loan('DISBURSEMENT', sm_loan_id, disbursement_reference_id, '',
#                                                      disbursement_message,
#                                                      'PROCEED', disbursement_message)
#                 # update_loan_info_status = hanlde_response_status(update_loan_info)
#                 if (update_loan_info == 200):
#                     logger.info(f"3-updated loan information with disbursement_ref_Id,{update_loan_info}")
#                     payload['partnerHandoffIntegration']['status'] = 'SUCCESS'
#                     payload['partnerHandoffIntegration']['partnerReferenceKey'] = disbursement_reference_id
#                     result = payload
#                 else:
#                     # loan_update_error = hanlde_response_body(update_loan_info)
#                     logger.error(f"3a-failure fecthing disbursement_id - 447 - {loan_update_error}")
#                     result = JSONResponse(status_code=500, content=loan_update_error)
#                     payload['partnerHandoffIntegration']['status'] = 'FAILURE'
#                     payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
#                     result = payload


#                 result = payload
#             else:
#                 payload['partnerHandoffIntegration']['status'] = 'FAILURE'
#                 payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
#                 nac_disbursement_response_body_message = nac_disbursement_response_body.get('content').get('message')
               
#                 logger.error(f"3b-Issue with post_disbursement_automator_data function 460, {nac_disbursement_response_body_message}")
#                 update_loan_info = await update_loan('DISBURSEMENT', sm_loan_id, '', 'Rejected',
#                                                      nac_disbursement_response_body_message,
#                                                      'PROCEED', nac_disbursement_response_body_message)
#                 # update_loan_info_status = hanlde_response_status(update_loan_info)
#                 if (update_loan_info == 200):

#                     payload['partnerHandoffIntegration']['status'] = 'FAILURE'
#                     payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
#                     result = payload
#                 else:
#                     # loan_update_error = hanlde_response_body(update_loan_info)
#                     logger.error(f"post_sanction_automator_data - 472 - {loan_update_error}")
#                     result = JSONResponse(status_code=500, content=loan_update_error)
#                     payload['partnerHandoffIntegration']['status'] = 'FAILURE'
#                     payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
#                     result = payload
#                 result = JSONResponse(status_code=500, content={"message": f"Issue with post_disbursement_automator_data function"})
#         else:
           
#             logger.error(f"Issue with post_disbursement_automator_data function - 480")
#             result = JSONResponse(status_code=500, content={"message": f"Issue with post_disbursement_automator_data function"})
#     except Exception as e:
#         logger.exception(f"Issue with post_disbursement_automator_data function, {e.args[0]}")
#         result = JSONResponse(status_code=500, content={"message": f"Issue with post_disbursement_automator_data function, {e.args[0]}"})
#     return result



async def perdix_update_loan(loan_data):
    """ Generic put Method to update perdix customer """
    try:
        
        
        url = validate_url + f'/api/individualLoan'
        str_url = str(url)
        login_token = await perdix_post_login()
        print("login_token",login_token.content)
        login_token_decode = generics.response_bytes_to_dict(login_token)
        # fetch_loan_response_decode_status = login_token_decode.get('status_code')
        login_token = login_token_decode.get('access_token')
        # If login is success
        headers = {
                "Content-Type": "application/json",
                "Content-Length": "0",
                "User-Agent": 'My User Agent 1.0',
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Authorization": f"bearer {login_token}"
            }
       
        loan_update_response = requests.put(url, json=loan_data, headers=headers)
        print("loan_update_response",loan_update_response)
        loan_update_response_dict = generics.response_to_dict(loan_update_response)

        
        
        
        
        api_call_duration = str(loan_update_response.elapsed.total_seconds()) + ' sec'
        str_data = str(loan_update_response_dict)
        info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
            channel='NorthernArc',
            request_url=url,
            request_method='POST',
            params="",
            request_body=str(str_data),
            response_body=str(info),
            status_code=str(loan_update_response.status_code),
            api_call_duration=api_call_duration,
            request_time=str(datetime.now())
        )
        await api_logs.insert(log_info)
        return loan_update_response_dict
    except Exception as e:
        logger.exception(f"GATEWAY - NORTHERNARC - PERDIX UPDATE LOAN - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

           

async def download_file_from_stream(
    doc_id: str
):
    """genric method for download file from stream url"""
    try:
        
        url = validate_url + f'/api/stream/{doc_id}'
      

        download_file_response = requests.get(url)
       
        
        download_file_response_headers = download_file_response.headers
        download_file_response_headers_content = download_file_response_headers.get('Content-Disposition')
        find_filename = download_file_response_headers_content.split('filename=', 1)
        found_filename = find_filename[1]
        found_file_ext = found_filename.split('.')
        new_file_name = doc_id + '.' + found_file_ext[1]
            

        file_path = os.path.abspath(('./static/'))

        with open(new_file_name, 'wb') as f:
            f.write(download_file_response.content)
            basename = f.name
            
            move_item = shutil.copy(basename, file_path)
            
            if os.path.exists(move_item):
                remove = os.remove(basename)
            else:
                
                
                move_item = shutil.move(basename, file_path)
        api_call_duration = str(download_file_response.elapsed.total_seconds()) + ' sec'
        # info = (str_data[:4950] + '..') if len(str_data) > 4950 else str_data
        log_info = LogBase(
                channel='northernarc',
                request_url=url,
                request_method='GET',
                params=f"{doc_id}",
                request_body="",
                response_body="",
                status_code=download_file_response.status_code,
                api_call_duration=api_call_duration,
                request_time=str(datetime.now()))
        await api_logs.insert(log_info)
        return new_file_name
           
       
            
       
    except Exception as e:
        logger.exception(f"GATEWAY - DOWNLOAD_FILE, {e.args[0]}")
        
        return JSONResponse(status_code=500,content={"message": f" {e.args[0]}"})

    