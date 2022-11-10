from fastapi import APIRouter,Depends
from dm_nac_service.schemas.dedupe import CreateDedupe
from fastapi.responses import JSONResponse
import dm_nac_service.schemas.dedupe as schema_dedupe
from dm_nac_service.schemas.dedupe import CreateDedupe
from dm_nac_service.models.dedupe import dedupe
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.services.dedupe as dedupe_service
from dm_nac_service.resource.generics import get_token_header

router = APIRouter(
    dependencies=[Depends(get_token_header)],
    tags=["Dedupe"],
)

@router.post("/dedupe", response_model=schema_dedupe.DedupeDB, tags=["Dedupe"])
async def find_dedupe(
        loan_id:str
) -> schema_dedupe.DedupeDB:
    """post method for find dedupe details"""
    try:
        find_dedupe_response = await dedupe_service.find_dedupe(loan_id)
        return find_dedupe_response
    except Exception as e:
        logger.exception(f"routes - dedupe - find_dedupe - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
        

@router.post("/create-dedupe")
async def create_dedupe(request_info: CreateDedupe):
    try:
        payload = request_info
        create_dedupe_response = await dedupe_service.create_dedupe(payload)
        return create_dedupe_response
    except Exception as e:
        logger.exception(f"routes - dedupe - create_dedupe - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
