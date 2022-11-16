from fastapi.responses import JSONResponse
from datetime import datetime
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.northernarc as nac_gateway
import dm_nac_service.gateway.perdix as perdix_gateway
import dm_nac_service.repository.sanction as sanction_repo
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction
import dm_nac_service.resource.generics as generics
from dm_nac_service.services.dedupe import find_dedupe


async def find_loan_id_from_sanction(
        customer_id:str
):
    """function for fetch loan_id from sanction table"""
    try:
        database = get_database()
        select_query = sanction.select().where(sanction.c.customer_id == customer_id).order_by(sanction.c.id.desc())
        raw_sanction = await database.fetch_one(select_query)
        sanction_dict = {
            "loanId": raw_sanction[60]
        }
        result = JSONResponse(status_code=200, content=sanction_dict)
    except Exception as e:
        logger.exception(f"Issue with find_dedupe function, {e.args[0]}")
        db_log_error = {"error": 'DB', "error_description": 'Customer ID not found in DB'}
        result= JSONResponse(status_code=500, content=db_log_error)
    return result
    

async def find_sanction(loan_id):
    try:
        database = get_database()
        select_query = sanction.select().where(sanction.c.loan_id == loan_id).order_by(sanction.c.id.desc())
        raw_sanction = await database.fetch_one(select_query)
        sanction_dict = {
            "customerId": raw_sanction[3],
            "dedupeRefId": raw_sanction[11],
            "sanction_ref_id":raw_sanction[8]
        }
        result = JSONResponse(status_code=200, content=sanction_dict)
    except Exception as e:
        logger.exception(f"{datetime.now()} - Issue with find_dedupe function, {e.args[0]}")
        db_log_error = {"error": 'DB', "error_description": 'Customer ID not found in DB'}
        result = JSONResponse(status_code=500, content=db_log_error)
    return result



async def sanction_service(sanction_data):
    try:
        sm_loan_id = sanction_data.get('loanId')
        fetch_dedupe_info = await find_dedupe(sm_loan_id)
        fetch_dedupe_info_status=generics.hanlde_response_status(fetch_dedupe_info)
        fetch_dedupe_info_body=generics.hanlde_response_body(fetch_dedupe_info)
        if(fetch_dedupe_info_status == 200):
            logger.info(f"2-Dedupe refrence_id,{fetch_dedupe_info_body}")
            dedupe_reference_id = fetch_dedupe_info_body.get('dedupeRefId')          
            sanction_data['dedupeReferenceId'] = int(dedupe_reference_id)
            sanction_dict = sanction_data
            logger.info(f'3 - Posting data to NAC create sanction endpoint, {sanction_dict}')
            sanction_response = await nac_gateway.nac_sanction(sanction_dict)         
            if sanction_response.status_code!=200:         
                return JSONResponse(status_code=500,
                                    content={"message": f"Unable to create sanction in northernarc"})          
            sanction_response_dict= generics.response_bytes_to_dict(sanction_response)
            await sanction_repo.insert(sanction_response_dict,sanction_dict)
            return sanction_response
    except Exception as e:
        logger.exception(f"services - sanction-sanction_service- {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


async def file_upload_service(customer_id, file, file_type):
    try:
        file_upload_service_response = await nac_gateway.nac_file_upload(customer_id, file, file_type)      
        if file_upload_service_response is None:          
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to upload file in northernarc"})       
        await sanction_repo.insert_file_reponse(file_upload_service_response)
        return file_upload_service_response
    except Exception as e:
        logger.exception(f"services - sanction- file_upload_service - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


async def get_sanction_status(customer_id):
    try:      
        get_sanction_status_response = await nac_gateway.get_sanction_status(customer_id)
        if get_sanction_status_response.status_code!=200:
            logger.error("unable to get sanction status response ")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to  get sanction status response in northernarc"})
        get_sanction_status_response_dict= generics.response_to_dict(get_sanction_status_response)
        await sanction_repo.insert_get_sanction_status(customer_id,get_sanction_status_response_dict)
        return get_sanction_status_response_dict
    except Exception as e:
        logger.exception(f"services - sanction-get_sanction_status {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def download_file_from_stream_service(doc_id):
    try:
        get_download_file_from_stream_response = await perdix_gateway.download_file_from_stream(doc_id)
        if get_download_file_from_stream_response.status_code!=200:
            logger.error("unable to download file from stream service")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to create download file stream in northernarc"})
        get_download_file_from_stream_response_dict= generics.response_to_dict(get_download_file_from_stream_response)      
        return get_download_file_from_stream_response_dict
    except Exception as e:
        logger.exception(f"services - sanction-download-file-stream  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})