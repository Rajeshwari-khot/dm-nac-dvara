from fastapi.responses import JSONResponse
import dm_nac_service.gateway.northernarc as collect_nac_gateway
from dm_nac_service.resource.generics import response_to_dict
from dm_nac_service.gateway.northernarc import file_upload_gateway
import dm_nac_service.repository.collect as collect_repo
from dm_nac_service.resource.log_config import logger




async def collect_services(collect_data_dict):
    try:
        collect_response = await collect_nac_gateway.collect_gateway(collect_data_dict)

        await collect_repo.insert(collect_response)
        return collect_response
    except Exception as e:
        logger.exception(f"SERVICES-AGENTS-{e.args[0]}")
        return JSONResponse(status_code=500,
                            content={"message": f"SERVICES - AGENTS - {e.args[0]}"})