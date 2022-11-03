from fastapi.responses import JSONResponse
from email import message
from http import client
from fastapi.responses import JSONResponse
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction
from dm_nac_service.models.sanction import sanction_fileupload
import dm_nac_service.models.sanction as sanction_model
from dm_nac_service.models.collect import collect
from dm_nac_service.resource.logging_config import logger

async def insert(collect_object):
    try:
        collect_demand_amount=collect_object.get('demandAmount')
        collect_demand_date=collect_object.get('demandDate')
        collect_instrument_type=collect_object.get('instrumentType')
        collect_partner_loand_id=collect_object.get('partnerLoandId')
        collect_reference=collect_object.get('reference')
        collect_repaymentAmount=collect_object.get('repaymentAmount')
        collect_repaymentDate=collect_object.get('repaymentDate')
        collect_settlementDate=collect_object.get('settlementDate')
        collect_tdsAmount=collect_object.get('tdsAmount')
        collect_outstandingAmount=collect_object.get('outstandingAmount')
        collect_transactionName=collect_object.get('transactionName')
        database = get_database()
        query= collect.insert().values(demand_amount=collect_demand_amount,
                                        demand_date=collect_demand_date,
                                         instrument_type=collect_instrument_type,
                                         partner_loan_id=collect_partner_loand_id,
                                         reference=collect_reference,
                                         repayment_amount=collect_repaymentAmount,  
                                         repayment_date= collect_repaymentDate,
                                         settlement_date= collect_settlementDate , 
                                         tds_amount= collect_tdsAmount,
                                         outstanding_amount=collect_outstandingAmount,
                                         transaction_name=collect_transactionName  )

        await database.execute(query)
        logger.info(f"COLLECT  INFO LOG SUCCESSFULLY INSERTED INTO COLLECT TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY - COLLECT- INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})                                 