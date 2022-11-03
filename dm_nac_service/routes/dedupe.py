from fastapi import APIRouter, status


# from dm_nac_service.resource.exceptions import _raiseException
from dm_nac_service.schemas.dedupe import CreateDedupe

from fastapi.responses import JSONResponse
import dm_nac_service.schemas.dedupe as schema_dedupe
from dm_nac_service.schemas.dedupe import CreateDedupe
from dm_nac_service.models.dedupe import dedupe
from dm_nac_service.config.database import get_database
from dm_nac_service.resource.logging_config import logger

from dm_nac_service.services.dedupe import dedupe_service

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    tags=["Dedupe"],
)

@router.post("/dedupe", response_model=schema_dedupe.DedupeDB, tags=["Dedupe"])
async def find_dedupe(
        loan_id
) -> schema_dedupe.DedupeDB:
    """post method for get dedupe details"""
    try:
        
        database = get_database()
        select_query = dedupe.select().where(dedupe.c.loan_id == loan_id).order_by(dedupe.c.id.desc())
        raw_dedupe = await database.fetch_one(select_query)
        dedupe_dict = {
            "dedupeRefId": raw_dedupe[1],
            "isDedupePresent": raw_dedupe[12],
            # "isEligible": raw_dedupe[18],
            # "message": raw_dedupe[19]
        }
       
        result = JSONResponse(status_code=200, content=dedupe_dict)
    except Exception as e:
        logger.exception(f"Issue with find_dedupe function, {e.args[0]}")
        
        db_log_error = {"error": 'DB', "error_description": 'Dedupe Reference ID not found in DB'}
        result = JSONResponse(status_code=500, content=db_log_error)
    return result

@router.post("/create-dedupe")
async def create_dedupe(request_info: CreateDedupe,
                                #   x_token: str = Depends(generics.get_token_header),
                                ):
    try:
       
        payload = request_info.dict()
       
        create_dedupe_response = await dedupe_service(payload)
       
        return create_dedupe_response

    except Exception as e:
        logger.exception(f"routes - dedupe - create_dedupe - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
