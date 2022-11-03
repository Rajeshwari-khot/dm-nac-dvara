
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.northernarc as nac_gateway
from fastapi.responses import JSONResponse
import dm_nac_service.repository.disbursement as disbursement_repo
from dm_nac_service.config.database import get_database
import dm_nac_service.resource.generics as generics
from dm_nac_service.models.disbursement import disbursement
from dm_nac_service.models.sanction import sanction



async def disbursement_service(disbursement_data):
   try:
        disbursement_response=await nac_gateway.nac_disbursement('disbursement',disbursement_data)
     #    if disbursement_response.status_code!= 200:
     #        return JSONResponse(status_code=500,
     #                             content={"message": f"Unable to create disbursement in northernarc"})
        
     #     disbursement_context_dict = generics.response_to_dict(disbursement_response)
        await disbursement_repo.insert(disbursement_response)
        return disbursement_response

   except Exception as e:
        logger.exception(f"services - disbursement -disbursement_service  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


