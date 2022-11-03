from fastapi import APIRouter, Depends


# from dm_nac_service.resource.exceptions import _raiseException


from fastapi.responses import JSONResponse


from dm_nac_service.schemas.disbursement import CreateDisbursement
from dm_nac_service.models.dedupe import dedupe
from dm_nac_service.models.sanction import sanction
from dm_nac_service.config.database import get_database
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.repository.disbursement as disbursement_repo
import dm_nac_service.resource.generics as generics
from dm_nac_service.services.disbursement import disbursement_service
from dm_nac_service.models.disbursement import disbursement
import dm_nac_service.services.perdix as perdix_service
router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    tags=["Disbursement"],
)






@router.post("/create-disbursement")
async def create_disbursement(request_info: CreateDisbursement,
                                #   x_token: str = Depends(generics.get_token_header),
                                ):
    try:
       
        payload = request_info.dict()
        
        create_disbursement_response = await disbursement_service(payload)
        
        return create_disbursement_response

    except Exception as e:
        logger.exception(f"routes - disbursement - create_disbursement - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})





@router.post("/disbursement/update-disbursement-in-db", tags=["Perdix"])
async def update_disbursement_status():
    try:
        update_disbursement_status_response=await perdix_service.update_disbursement_status()
        

    except Exception as e:
        logger.exception(f"routes - Disbursment - update_disbursement_status - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
