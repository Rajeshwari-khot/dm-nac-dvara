from fastapi import APIRouter
from fastapi.responses import JSONResponse
import dm_nac_service.services.disbursement_status as disbursement_status_service
from dm_nac_service.resource.logging_config import logger
router = APIRouter(
    # dependencies=[Depends(get_token_header)]
    tags=["Disbursement"]
)

@router.get("/get-disbursement-status/{disbursement_reference_id}")

async def get_disbursement_status(disbursement_reference_id:str
                                ):
    try:
        get_disbursment_status_response= await disbursement_status_service.get_disbursement_status(disbursement_reference_id)
        return get_disbursment_status_response
    except Exception as e:
        logger.exception(f"routes - disbursement - get_disbursement_status - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

