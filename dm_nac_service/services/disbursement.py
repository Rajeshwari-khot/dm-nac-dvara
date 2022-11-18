
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.northernarc as nac_gateway
from fastapi.responses import JSONResponse
import dm_nac_service.repository.disbursement as disbursement_repo
import dm_nac_service.resource.generics as generics


async def create_disbursment(disbursement_data):
      try:
            disbursement_response=await nac_gateway.nac_disbursement(disbursement_data)                     
            await disbursement_repo.insert(disbursement_response,disbursement_data)
            return disbursement_response
      except Exception as e:
        logger.exception(f"services - disbursement -create_disbursment  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})
        
       
async def get_disbursement_status(disbursement_reference_id):
    try:      
        get_disbursement_status_response = await nac_gateway.get_disbursement_status(disbursement_reference_id)
        await disbursement_repo.insert_get_disbursement_status(disbursement_reference_id,get_disbursement_status_response)
        return get_disbursement_status_response
    except Exception as e:
        logger.exception(f"services - disbursement-get_disbursement_status {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


     