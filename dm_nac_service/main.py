# pylint: disable=import-error
"""main module"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
# data
from dm_nac_service.models.dedupe import dedupe_metadata
from dm_nac_service.models.disbursement import disbursement_metadata
from dm_nac_service.models.sanction import sanction_metadata
from dm_nac_service.models.collect import collect_metadata


from dm_nac_service.models.logs import logs_metadata
import dm_nac_service.config.database as config
# router
from dm_nac_service.routes.dedupe import router as dedupe_router
from dm_nac_service.routes.disbursement import router as disbursment_router
from dm_nac_service.routes.disbursement_status import router as disbursment_status_router
from dm_nac_service.routes.sanction import router as sanction_router
from dm_nac_service.routes.perdix import router as perdix_router

from dm_nac_service.routes.collect import router as collect_router


# utils
from dm_nac_service.utils import get_env_or_fail




origins = ["*"]


app = FastAPI(title="Perdix-BBPS",
              debug=True,
    description='Axis BBPS',
    version="0.0.1",
    terms_of_service="http://dvara.com/terms/",
    contact={
        "name": "BBPS Integration",
        "url": "https://hackmd.io/@aayushm/BJVbXGhp_#Axis-BBPS-API-Approach-Document",
        "email": "contact@dvara.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)


SCHEDULER_TIME = 'scheduler-time'

scheduler_start_in_seconds = get_env_or_fail(
    SCHEDULER_TIME, 'start-seconds', SCHEDULER_TIME + ' start-seconds not configured')
scheduler_end_in_seconds = get_env_or_fail(
    SCHEDULER_TIME, 'end-seconds', SCHEDULER_TIME + ' end-seconds not configured')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """async function for startup"""
    await config.get_database().connect()
    dedupe_metadata.create_all(config.sqlalchemy_engine)
    disbursement_metadata.create_all(config.sqlalchemy_engine)
    sanction_metadata.create_all(config.sqlalchemy_engine)
    logs_metadata.create_all(config.sqlalchemy_engine)
    collect_metadata.create_all(config.sqlalchemy_engine)


@app.on_event("startup")
@repeat_every(seconds=int(scheduler_start_in_seconds) * int(scheduler_end_in_seconds))  # 1 minute
async def update_payments_task() -> str:
    """async function for scheduler start"""
    # await update_payment_status()
    print('Schedulers Running')
    return "Schedulers Running"


@app.on_event("shutdown")
async def shutdown():
    """async function for shutdown"""
    await config.get_database().disconnect()


app.include_router(dedupe_router, prefix="")
app.include_router(disbursment_router, prefix="")
app.include_router(disbursment_status_router, prefix="")
app.include_router(sanction_router, prefix="")
app.include_router(perdix_router, prefix="")
app.include_router(collect_router, prefix="")





if __name__ == "__main__":
    """uvicorn run"""
    uvicorn.run(app, host="0.0.0.0", port=9029)
