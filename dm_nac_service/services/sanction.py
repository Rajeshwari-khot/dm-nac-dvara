from fastapi.responses import JSONResponse
import  dm_nac_service.resource.generics as generics
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.repository.sanction as sanction_repo
from dm_nac_service.gateway.northernarc import nac_sanction
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction

async def find_loan_id_from_sanction(
        customer_id:str
):
    """function for fetch loan_id from sanction table"""
    try:
        database = get_database()
        select_query = sanction.select().where(sanction.c.customer_id == customer_id).order_by(sanction.c.id.desc())
       
        raw_sanction = await database.fetch_one(select_query)
        print("raw_sanction",raw_sanction)

        sanction_dict = {
            "loanId": raw_sanction[60]
        }

        result = JSONResponse(status_code=200, content=sanction_dict)
    except Exception as e:
        logger.exception(f"Issue with find_dedupe function, {e.args[0]}")

        db_log_error = {"error": 'DB', "error_description": 'Customer ID not found in DB'}
        result = JSONResponse(status_code=500, content=db_log_error)
    return result
    

async def sanction_service(payload):
    try:
        sanction_response = await nac_sanction(payload)
        if sanction_response.status_code!=200:
            logger.error("unable to get sanction content")
            return JSONResponse(status_code=500,
                                 content={"message": f"Unable to create sanction in northernarc"})
        sanction_response_dict= generics.response_to_dict(sanction_response)
        await sanction_repo.insert(sanction_response_dict)
        return sanction_response_dict
    except Exception as e:
        logger.exception(f"services - sanction  - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})