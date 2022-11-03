from fastapi.responses import JSONResponse
from dm_nac_service.schemas.dedupe import DedupeTableBase
from dm_nac_service.resource.logging_config import logger

def _raiseException(module, function, args):
    logger.exception(f"{module} - {function} - {args}")
    api_error = DedupeTableBase(status='FAILURE', errorCode='03')
    return JSONResponse(status_code=500, content=api_error.dict())