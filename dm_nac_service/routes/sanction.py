from fastapi import APIRouter, status


# from dm_nac_service.resource.exceptions import _raiseException
from dm_nac_service.schemas.dedupe import CreateDedupe

from fastapi.responses import JSONResponse
import dm_nac_service.schemas.sanction as sanction_schema
from dm_nac_service.schemas.dedupe import CreateDedupe
from dm_nac_service.models.dedupe import dedupe
from dm_nac_service.config.database import get_database
from dm_nac_service.resource.logging_config import logger

from dm_nac_service.services.sanction import sanction_service
router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    tags=["sanction"],
)



@router.post("/sanction", tags=["Sanction"])
async def create_sanction(request_info : sanction_schema.CreateSanction):
    try:
        payload = request_info.dict()
        create_sanction_response = await sanction_service(payload)
        return create_sanction_response
    except Exception as e:
        logger.exception(f"routes - sanction - create_sanction - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
