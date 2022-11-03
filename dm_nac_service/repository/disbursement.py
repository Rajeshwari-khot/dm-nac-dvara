# data

from dm_nac_service.config.database import get_database
from fastapi.responses import JSONResponse
import dm_nac_service.models.disbursement as disbursement_model

from dm_nac_service.resource.logging_config import logger


async def insert(disbursement_object):
    try:
        
        disbursement_reference_id=disbursement_object.get('content').get('value').get('disbursementReferenceId')
        disbursement_status = disbursement_object.get('content').get('status')
        disbursement_stage = disbursement_object.get('content').get('value').get('stage')
        disbursement_utr = disbursement_object.get('content').get('value').get('utr')
        disbursement_message = disbursement_object.get('content').get('message')
        disbursement_status1 = disbursement_object.get('content').get('value').get('disbursementStatus')
        disbursement_originator_id = disbursement_object.get('originator_id')
        disbursement_sanction_reference_id=disbursement_object.get('sanctionReferenceId')
        disbursement_customer_id=disbursement_object.get('customerId')
        disbursement_requested_amount=disbursement_object.get('requested_amount')
        disbursement_ifsc_code = disbursement_object.get('ifsc_code')
        disbursement_branch_name = disbursement_object.get('branch_name')
        disbursement_processing_fees=disbursement_object.get('processing_fees')
        disbursement_insurance_amount = disbursement_object.get('insurance_amount')
        disbursement_date = disbursement_object.get('disbursement_date')

        database = get_database()
        query =disbursement_model.disbursement.insert().values(disbursement_reference_id=str(disbursement_reference_id),
                                                    disbursement_status=disbursement_status,
                                                    stage=disbursement_stage,
                                                    utr=str(disbursement_utr),
                                                    message=disbursement_message,
                                                    status=disbursement_status1,
                                                    originator_id=disbursement_originator_id,
                                                    sanction_reference_id=str(disbursement_sanction_reference_id),
                                                    customer_id=disbursement_customer_id,
                                                    requested_amount=disbursement_requested_amount,
                                                    ifsc_code=disbursement_ifsc_code,
                                                    branch_name=str(disbursement_branch_name),
                                                    processing_fees=disbursement_processing_fees,
                                                    insurance_amount=str(disbursement_insurance_amount),
                                                    disbursement_date=str(disbursement_date)
                                            )
        await database.execute(query)
        logger.info(f"DISBURSEMENT INFO SUCCESSFULLY INSERTED INTO DISBURSEMENT TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY -DISBURSEMENT - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

        
    
        