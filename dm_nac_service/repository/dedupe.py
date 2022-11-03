# data

from dm_nac_service.config.database import get_database
from fastapi.responses import JSONResponse
import dm_nac_service.models.dedupe as dedupe_model

from dm_nac_service.resource.logging_config import logger


async def insert(dedupe_object):
    try:
        
        dedupe_dict=dedupe_object['dedupeRequestSource']
        dedupe_loan_id = dedupe_dict.get('loanId')
        dedupe_customer_name = dedupe_dict.get('customerName')
        dedupe_date_of_birth = dedupe_dict.get('dateOfBirth')
        dedupe_contact_number = dedupe_dict.get('contactNumber')
        dedupe_id_type1 = dedupe_dict['kycDetailsList'][0]['type']
        dedupe_id_value1=dedupe_dict['kycDetailsList'][0]['value']
        dedupe_id_type2=dedupe_dict['kycDetailsList'][1]['type']
        dedupe_id_value2=dedupe_dict['kycDetailsList'][1]['value']
        dedupe_account_number = dedupe_dict.get('accountNumber')
        dedupe_pin_code = dedupe_dict.get('pincode')
        dedupe_result=dedupe_object.get('results')
        dedupe_response_type = dedupe_object.get('type')
        dedupe_reference_id = dedupe_object.get('dedupeReferenceId')
        is_dedupe_present = dedupe_object.get('isDedupePresent')
        database = get_database()
        query =dedupe_model.dedupe.insert().values(dedupe_reference_id=str(dedupe_reference_id),
                                                    account_number=dedupe_account_number,
                                                    contact_number=dedupe_contact_number,
                                                    customer_name=dedupe_customer_name,
                                                    dob=dedupe_date_of_birth,
                                                    id_type1=dedupe_id_type1,
                                                    id_value1=dedupe_id_value1,
                                                    id_type2=dedupe_id_type2,
                                                    id_value2=dedupe_id_value2,
                                                    loan_id=dedupe_loan_id,
                                                    pincode=dedupe_pin_code,
                                                    dedupe_present=str(is_dedupe_present),
                                                    response_type=dedupe_response_type,
                                                    dedupe_results=str(dedupe_result)
                                            )
        await database.execute(query)
        logger.info(f"DEDUPE INFO SUCCESSFULLY INSERTED INTO DEDUPE TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY -DEDUPE - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

        
    
        