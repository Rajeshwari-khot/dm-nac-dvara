from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.sql import and_, or_
from dm_nac_service.resource.log_config import logger
from dm_nac_service.gateway.northernarc import nac_sanction
import dm_nac_service.gateway.northernarc as sanction_gateway
import dm_nac_service.gateway.perdix as perdix_gateway
from dm_nac_service.resource.generics import response_to_dict
from dm_nac_service.gateway.northernarc import file_upload_gateway
import dm_nac_service.repository.sanction as sanction_repo
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction



async def find_sanction(loan_id):
    try:
        database = get_database()
        select_query = sanction.select().where(sanction.c.loan_id == loan_id).order_by(sanction.c.id.desc())
        raw_sanction = await database.fetch_one(select_query)
        sanction_dict = {
            "customerId": raw_sanction[3],
            "dedupeRefId": raw_sanction[11]
        }


        result = JSONResponse(status_code=200, content=sanction_dict)
    except Exception as e:
        logger.exception(f"{datetime.now()} - Issue with find_dedupe function, {e.args[0]}")

        db_log_error = {"error": 'DB', "error_description": 'Customer ID not found in DB'}
        result = JSONResponse(status_code=500, content=db_log_error)
    return result



async def sanction_service(payload):
    try:
        
        sanction_response = await nac_sanction(payload)
        
        
        if sanction_response.status_code!=200:
            logger.error("unable to get sanction content")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to create sanction in northernarc"})
        dedupe_reference_id=payload.get('dedupeReferenceId')
        sanction_response_dedupe=dedupe_reference_id
        # print("dedupe",sanction_response_dedupe)
        sanction_response_dict= response_to_dict(sanction_response)
        
        await sanction_repo.insert(sanction_response_dict,payload)
        return sanction_response
    except Exception as e:
        logger.exception(f"services - sanction  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


async def file_upload_service(customer_id, file, file_type):
    try:
        file_upload_service_response = await file_upload_gateway(customer_id, file, file_type)
        if file_upload_service_response is None:
            logger.error("unable to get file_upload")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to upload file in northernarc"})
        await sanction_repo.insert_file_reponse(file_upload_service_response)
        return file_upload_service_response
    except Exception as e:
        logger.exception(f"services - sanction  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


async def get_sanction_service(customer_id):
    try:
        get_sanction_status_response = await sanction_gateway.get_nac_sanction(customer_id)
        if get_sanction_status_response.status_code!=200:
            logger.error("unable to get sanction status content")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to create get sanction status in northernarc"})
        get_sanction_status_response_dict= response_to_dict(get_sanction_status_response)
        await sanction_repo.insert_get_sanction_status(customer_id,get_sanction_status_response_dict)
        return get_sanction_status_response_dict
    except Exception as e:
        logger.exception(f"services - sanction  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def download_file_from_stream_service(doc_id):
    try:
        get_download_file_from_stream_response = await perdix_gateway.download_file_from_stream(doc_id)
        if get_download_file_from_stream_response.status_code!=200:
            logger.error("unable to get sanction status content")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to create get sanction status in northernarc"})
        get_download_file_from_stream_response_dict= response_to_dict(get_download_file_from_stream_response)
        # await sanction_repo.insert_get_sanction_status(customer_id,get_sanction_status_response_dict)
        return get_download_file_from_stream_response_dict
    except Exception as e:
        logger.exception(f"services - sanction-upload-file-stream  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})