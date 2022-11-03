

from dm_nac_service.resource.logging_config import logger
from fastapi import APIRouter, status,Body
from fastapi.responses import JSONResponse

from dm_nac_service.routes.dedupe import create_dedupe
import dm_nac_service.services.perdix as perdix_service


router = APIRouter()


NAC_SERVER = 'northernarc-server'


@router.post("/nac-dedupe-automator-data", tags=["Automator"])
async def post_automator_data(
    
    request_info: dict = Body(...),

):
    try:
        payload=request_info
       
        post_automator_data_response=await perdix_service.post_automator_data_service(payload)
       
        return post_automator_data_response
       
    except Exception as e:
        logger.exception(f"routes - Perdix - post_automator_data - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


