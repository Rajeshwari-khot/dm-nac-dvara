
from dm_nac_service.resource.logging_config import logger
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
import dm_nac_service.services.perdix as perdix_service


router = APIRouter()
NAC_SERVER = 'northernarc-server'


@router.post("/nac-dedupe-automator-data", tags=["Automator"])
async def post_automator_data(    
    request_info: dict = Body(...),
):
    try:
        payload=request_info      
        post_automator_data_response=await perdix_service.post_dedupe_automator_data_service(payload)      
        return post_automator_data_response     
    except Exception as e:
        logger.exception(f"routes - Perdix - post_automator_data - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


@router.post("/nac-sanction-automator-data", tags=["Automator"])
async def post_sanction_automator_data(   
    request_info: dict = Body(...),
):
    try:
        payload=request_info      
        post_automator_data_response=await perdix_service.post_sanction_automator_data_service(payload)      
        return post_automator_data_response      
    except Exception as e:
        logger.exception(f"routes - Perdix - post_automator_data - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

    
@router.post("/sanction/update-sanction-in-db", tags=["Perdix"])
async def update_sanction_in_db():
    """post method for update sanction information in database"""
    """fetch remaining  data from sanction table using fetch_data_from_db """
    """send customer_id into nac_get_sanction function """
    """update data using update_loan function"""
    try:
        update_sanction_in_db_response = await perdix_service.update_sanction_status_in_db()
        return update_sanction_in_db_response
    except Exception as e:
        logger.exception(f"routes - Perdix - update_sanction_in_db - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})    

    
@router.post("/nac-disbursement-automator-data", tags=["Automator"])
async def post_disbursement_automator_data(   
    request_info: dict = Body(...),
):
    try:
        payload=request_info      
        post_disbursement_automator_data_response=await perdix_service.post_disbursement_automator_data(payload)      
        return post_disbursement_automator_data_response      
    except Exception as e:
        logger.exception(f"routes - Perdix - post_disbursement_automator_data - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


@router.post("/sanction/update-disbursement-in-db", tags=["Perdix"])
async def update_disbursement_in_db():
    """post method for update disbursement information in database"""
    """fetch remaining  data from disbursement table using fetch_data_from_db """
    """send customer_id into nac_get_disbursement function """
    """update data using update_loan function"""
    try:
        update_disbursement_in_db_response = await perdix_service.update_disbursement_in_db()
        return update_disbursement_in_db_response
    except Exception as e:
        logger.exception(f"routes - Perdix - update_disbursement_in_db - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})