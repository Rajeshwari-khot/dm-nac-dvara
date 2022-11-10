import json

from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.northernarc as nac_gateway
from fastapi.responses import JSONResponse
import dm_nac_service.repository.dedupe as dedupe_repo
from dm_nac_service.models.dedupe import dedupe
from dm_nac_service.config.database import get_database




async def find_dedupe(loan_id): 
    try:
        database = get_database()
        select_query = dedupe.select().where(dedupe.c.loan_id == loan_id).order_by(dedupe.c.id.desc())
        raw_dedupe = await database.fetch_one(select_query)       
        dedupe_dict = {
            "dedupeRefId": raw_dedupe[1],
            "isDedupePresent": raw_dedupe[12],
            "isEligible": raw_dedupe[18],
            "message": raw_dedupe[19]
        }      
        return JSONResponse(status_code=200, content=dedupe_dict)
    except Exception as e:
        logger.exception(f"services - dedupe -find-dedupe  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def create_dedupe(dedupe_data):
      try:
            dedupe_response=await nac_gateway.nac_dedupe(dedupe_data)
            if dedupe_response.status_code!= 200:
                  return JSONResponse(status_code=500,
                                    content={"message": f"Unable to create dedupe in northernarc"})
            response_content = dedupe_response.content
            dedupe_context_dict = json.loads(response_content.decode('utf-8'))
            dedupe_dict=dedupe_context_dict[0]
            await dedupe_repo.insert(dedupe_dict)
            return dedupe_response
      except Exception as e:
        logger.exception(f"services - dedupe -create_dedupe  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
        
       
        
     