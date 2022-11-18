from fastapi import APIRouter,Depends
from databases import Database
from fastapi.responses import JSONResponse
from dm_nac_service.schemas.disbursement import CreateDisbursement
import dm_nac_service.services.disbursement as disbursement_service 
from dm_nac_service.resource.logging_config import logger
from dm_nac_service.config.database import get_database
from dm_nac_service.resource.generics import get_token_header

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    tags=["Disbursement"],
)


@router.post("/create-disbursement")
async def create_disbursement(request_info: CreateDisbursement):
    try:
        payload = request_info
        create_disbursement_response = await disbursement_service.create_disbursment(payload)
        return create_disbursement_response
    except Exception as e:
        logger.exception(f"routes - disbursement - create_disbursement - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


@router.get("/disbursement-status")
async def disbursement_status(
        disbursement_reference_id: str, database: Database = Depends(get_database)
):
    """get method for disbursement_status"""
    """sent customer_id to northern_arc disbursement_status endpoint"""
    """get response as disbursement data for that disbursement_reference_id  """
    try:
        get_disbursement_response = await disbursement_service.get_disbursement_status(disbursement_reference_id)
        return get_disbursement_response
    except Exception as e:
        logger.exception(f"routes - get_disbursement_status - disbursement_status , {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})       
