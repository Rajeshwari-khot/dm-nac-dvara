from dm_nac_service.config.database import get_database
from fastapi.responses import JSONResponse
import dm_nac_service.models.disbursement as disbursement_model
from dm_nac_service.resource.logging_config import logger


async def insert(disbursement_object,payload):
    try:       
        disbursment_reference_id=disbursement_object.get('content').get('value').get('disbursementReferenceId')
        disbursement_message=disbursement_object.get('content').get('message')
        disbursement_status=disbursement_object.get('content').get('status')
        disbursement_originator_id=payload.get('originatorId')
        disbursement_sanction_reference_id=payload.get('sanctionReferenceId')
        disbursement_customer_id=payload.get('customerId')
        disbursement_requested_amount=payload.get('requestedAmount')
        disbursement_ifsc_code=payload.get('ifscCode')
        disbursement_branch_name=payload.get('branchName')
        disbursement_processing_fees=payload.get('processingFees')
        disbursement_insurance_amount=payload.get('insuranceAmount')
        disbursement_disbursement_date=payload.get('disbursementDate')

        database = get_database()
        query =disbursement_model.disbursement.insert().values(disbursement_reference_id=str(disbursment_reference_id),
                                                    message=disbursement_message,
                                                    status=disbursement_status,
                                                    originatorId=disbursement_originator_id,
                                                    sanctionReferenceId=disbursement_sanction_reference_id,
                                                    customerId=disbursement_customer_id,
                                                    requestedAmount=disbursement_requested_amount,
                                                    ifscCode=disbursement_ifsc_code,
                                                    branchName=disbursement_branch_name,
                                                    insuranceAmount=disbursement_insurance_amount,
                                                    processingFees=disbursement_processing_fees,
                                                    disbursementDate=disbursement_disbursement_date
                                                                                                   
                                            )
        await database.execute(query)
        logger.info(f"DISBURSEMENT INFO SUCCESSFULLY INSERTED INTO DISBURSEMENT TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY -DISBURSEMENT - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

        
    
        