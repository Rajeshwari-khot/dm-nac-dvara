from email import message
from http import client
from fastapi.responses import JSONResponse
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction


from dm_nac_service.resource.logging_config import logger
async def insert(sanction_object):
    try:
        print("sanction_object",sanction_object)
        sanction_message=sanction_object.get('content').get('message')
        sanction_status=sanction_object.get('content').get('status')
        sanction_customer_id=sanction_object.get('content').get('value').get('customerId')
        sanction_client_id=sanction_object.get('content').get('value').get('clientId')
        database = get_database()
        query = sanction.insert().values(message=sanction_message,
                                         status=sanction_status,
                                         customer_id=str(sanction_customer_id),
                                         client_id=sanction_client_id   )
        await database.execute(query)
        logger.info(f"sanction  INFO LOG SUCCESSFULLY INSERTED INTO SANCTION TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY - SANCTION - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})