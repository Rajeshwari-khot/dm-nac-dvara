from fastapi.responses import JSONResponse
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.northernarc as northern_arc_gateway
import dm_nac_service.repository.disbursement as disbursement_repo



async def get_disbursement_status(disbursement_reference_id):
    try:
        get_disbursement_status_in_northernarc= await northern_arc_gateway.get_disbursement_status('disbursement',disbursement_reference_id)
        await disbursement_repo.insert(get_disbursement_status_in_northernarc)
        return get_disbursement_status_in_northernarc
    except Exception as e:
        logger.exception(f"SERVICES - DISBURSEMENT STATUS - get_disbursement_status - {e.args[0]}")
        return JSONResponse(status_code=500,
                            content={"message": f"SERVICES - DISBURSEMENT STATUS  - get_disbursement_status- {e.args[0]}"})