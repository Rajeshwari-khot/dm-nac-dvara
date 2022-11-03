import json
from datetime import datetime
import dm_nac_service.schemas.dedupe as data_dedupe
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.northernarc as nac_gateway
from fastapi.responses import JSONResponse
import dm_nac_service.repository.dedupe as dedupe_repo
import dm_nac_service.resource.generics as generics
from dm_nac_service.resource.exceptions import _raiseException




async def dedupe_service(dedupe_data):
   try:
         
         dedupe_response=await nac_gateway.nac_dedupe('dedupe',dedupe_data)
         if dedupe_response.status_code!= 200:
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to create dedupe in northernarc"})
         response_content = dedupe_response.content
         dedupe_context_dict = json.loads(response_content.decode('utf-8'))
         dedupe_dict=dedupe_context_dict[0]
         await dedupe_repo.insert(dedupe_dict)
         return dedupe_context_dict

   except Exception as e:
        logger.exception(f"services - dedupe -dedupe_service  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
        
       
        
     