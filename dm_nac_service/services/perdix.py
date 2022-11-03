import json
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction
from fastapi.responses import JSONResponse
from fastapi import Body
from dm_nac_service.resource.logging_config import logger
import dm_nac_service.gateway.perdix as perdix_gateway
import dm_nac_service.gateway.northernarc as nac_gateway
import dm_nac_service.resource.generics as generics
from dm_nac_service.models.disbursement import disbursement
import dm_nac_service.routes.dedupe as dedupe_route
from dm_nac_service.services.sanction import find_loan_id_from_sanction
from dm_nac_service.services.dedupe import dedupe_service




async def update_loan(
    url_type: str,
    loan_id: int,
    reference_id: str,
    stage: str,
    reject_reason: str,
    loan_process_action: str,
    remarks: str
):
    """post function for update_loan"""
    """fetch data from genric post perdix_fetch_loan function """
    """send data to Method update perdix customer"""
    try:
        
        # For Real updating the loan information
        get_loan_info = await perdix_gateway.perdix_fetch_loan(loan_id)
        get_loan_info_dict=generics.response_bytes_to_dict(get_loan_info)
        
       
       
       
        if(get_loan_info.status_code == 200):
            get_loan_info=get_loan_info_dict
            if "rejectReason" in get_loan_info:
                get_loan_info['rejectReason'] = reject_reason
                
            get_loan_info['stage'] = stage
            if "remarks1" in get_loan_info:
                get_loan_info['remarks1'] = "Testing remarks1"
            if "loanProcessAction" in get_loan_info:
                get_loan_info['loanProcessAction'] = "Testing loanProcessAction"
            if "accountUserDefinedFields" in get_loan_info:
                if (url_type == 'DEDUPE'):
                    get_loan_info['accountUserDefinedFields']['userDefinedFieldValues']['udf41'] = reference_id
                    

                if (url_type == 'SANCTION'):
                    get_loan_info['accountUserDefinedFields']['userDefinedFieldValues']['udf42'] = reference_id

                if (url_type == 'SANCTION-REFERENCE'):
                    get_loan_info['accountUserDefinedFields']['userDefinedFieldValues']['udf43'] = reference_id

                if (url_type == 'DISBURSEMENT'):
                    get_loan_info['accountUserDefinedFields']['userDefinedFieldValues']['udf44'] = reference_id

                if (url_type == 'DISBURSEMENT-ITR'):
                    get_loan_info['accountUserDefinedFields']['userDefinedFieldValues']['udf45'] = reference_id
            if(stage == 'Rejected'):
                prepare_loan_info = {
                    "loanAccount": get_loan_info,
                    "loanProcessAction": loan_process_action,
                    "stage": stage,
                    "remarks": remarks,
                    "rejectReason": reject_reason
                }
            else:
                prepare_loan_info = {
                    "loanAccount": get_loan_info,
                    "loanProcessAction": loan_process_action,
                    "remarks": remarks,
                    "rejectReason": ''
                }

            # Below is for loan Id 317
            prepare_loan_info['loanAccount']['tenure'] = 24
            update_perdix_loan = await perdix_gateway.perdix_update_loan(prepare_loan_info)
            
            perdix_update_loan_response_decode_status = generics.hanlde_response_status(update_perdix_loan)
           
            loan_response_decode_body = generics.hanlde_response_body(update_perdix_loan)
           
            if(perdix_update_loan_response_decode_status == 200):
                logger.info(f"updating perdix loan'{loan_response_decode_body}")
                result = JSONResponse(status_code=200, content=loan_response_decode_body)
            else:
                logger.error(f"failed to update_loan in perdix - 559 - {loan_response_decode_body}")
                result = JSONResponse(status_code=404, content=loan_response_decode_body)

        else:
            logger.error(f"failed to update_loan - 563 - {loan_response_decode_body}")
            result = JSONResponse(status_code=404, content=loan_response_decode_body)
            
    except Exception as e:
        logger.exception(f"GATEWAY - NORTHERNARC - PERDIX UPDATE LOAN - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def update_disbursement_status():
   try:
        database = get_database()
        database_record_fetch = await generics.fetch_data_from_db(disbursement)
       
        
        for i in database_record_fetch:
            disbursement_ref_id = i[1]
            sanction_ref_id = i[8]
            customer_id = i[9]
            
            disbursement_sanction_id = await find_loan_id_from_sanction(customer_id)
            
           
            disbursement_sanction_id_status = generics.hanlde_response_status(disbursement_sanction_id)
            disbursement_sanction_id_body = generics.hanlde_response_body(disbursement_sanction_id)
            
            if(disbursement_sanction_id_status == 200):
               
                sm_loan_id = disbursement_sanction_id_body.get('loanId')
               
                get_disbursement_response = await nac_gateway.get_disbursement_status('disbursement', disbursement_ref_id)
                
                
                if(get_disbursement_response == 200):
                    logger.info(f"1-disbursement response ,{get_disbursement_response}")
                    get_disbursement_response_content = get_disbursement_response['content']
                    get_disbursement_response_status = get_disbursement_response['content']['status']
                    if (get_disbursement_response_status == 'SUCCESS'):
                       
                        get_disbursement_response_stage = get_disbursement_response['content']['value']['stage']
                        
                        if (get_disbursement_response_stage == 'AMOUNT_DISBURSEMENT'):
                            get_disbursement_response_utr = get_disbursement_response['content']['value']['utr']
                            get_disbursement_response_disbursement_status = \
                            get_disbursement_response['content']['value'][
                                'disbursementStatus']
                            query = disbursement.update().where(
                                disbursement.c.disbursement_reference_id == disbursement_ref_id).values(
                                status=get_disbursement_response_status,
                                stage=get_disbursement_response_stage,
                                disbursement_status=get_disbursement_response_disbursement_status,
                                message='',
                                utr=get_disbursement_response_utr)
                            disbursement_updated = await database.execute(query)
                            update_loan_info = await update_loan('DISBURSEMENT-ITR', sm_loan_id,
                                                                 get_disbursement_response_utr, 'Dedupe',
                                                                 get_disbursement_response_disbursement_status,
                                                                 'PROCEED',
                                                                 get_disbursement_response_disbursement_status)
                           
                        else:
                            get_disbursement_response_disbursement_status = get_disbursement_response['content']['value']['disbursementStatus']
                            query = disbursement.update().where(
                                disbursement.c.disbursement_reference_id == disbursement_ref_id).values(
                                status=get_disbursement_response_status,
                                stage=get_disbursement_response_stage,
                                disbursement_status=get_disbursement_response_disbursement_status,
                                message='',
                                utr='')
                            disbursement_updated = await database.execute(query)
                            
                    else:
                        if ("value" in get_disbursement_response_content):

                            get_disbursement_response_stage = get_disbursement_response['content']['value']['stage']
                            get_disbursement_response_value_status = get_disbursement_response['content']['value'][
                                'status']
                            query = disbursement.update().where(
                                disbursement.c.disbursement_reference_id == disbursement_ref_id).values(
                                status=get_disbursement_response_status,
                                stage=get_disbursement_response_stage,
                                disbursement_status=get_disbursement_response_value_status,
                                message='',
                                utr='')
                            disbursement_updated = await database.execute(query)
                            
                            update_loan_info = await update_loan('DISBURSEMENT-ITR', sm_loan_id,
                                                                 '', 'Rejected',
                                                                 get_disbursement_response_stage,
                                                                 'PROCEED',
                                                                 get_disbursement_response_stage)
                        else:
                            get_disbursement_response_message = get_disbursement_response['content']['message']
                            query = disbursement.update().where(
                                disbursement.c.disbursement_reference_id == disbursement_ref_id).values(
                                status=get_disbursement_response_status,
                                stage='',
                                disbursement_status='',
                                message=get_disbursement_response_message,
                                utr='')
                            disbursement_updated = await database.execute(query)
                            
                            update_loan_info = await update_loan('DISBURSEMENT-ITR', sm_loan_id,
                                                                 '', 'Rejected',
                                                                 get_disbursement_response_stage,
                                                                 'PROCEED',
                                                                 get_disbursement_response_stage)
                    result = database_record_fetch
                else:
                    logger.error(f" Error from update_disbursement_in_db-795, {get_disbursement_response}")
                    result = JSONResponse(status_code=500, content=get_disbursement_response)
            else:
                logger.error(f"failed fetch the customer id from update_disbursement_in_db sanction {disbursement_sanction_id_body}")
                result = JSONResponse(status_code=500, content=disbursement_sanction_id_body)
                continue

   except Exception as e:
        logger.exception(f"services - perdix - update_disbursement_status - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def post_automator_data_service(
    
   payload

):
    """Function to prepare user data from perdix automator """
    """post into create_dedpue function"""
    """update response back to the perdix using update_loan function"""
    try:
        
        
        
        # Data Preparation to post the data to NAC dedupe endpoint
        customer_data = payload["enrollmentDTO"]["customer"]
        loan_data = payload["loanDTO"]["loanAccount"]
        first_name = customer_data.get("firstName")
       
        middle_name=customer_data.get("middleName")
        last_name = customer_data.get("lastName")
        first_name = first_name if first_name else ""
        middle_name = middle_name if middle_name else ""
        last_name = last_name if last_name else ""
        
        if middle_name and last_name != None :
            full_name = first_name + " " + middle_name + " " + last_name
        elif middle_name == None or last_name !=None :
            full_name = first_name +middle_name + " " + last_name
        elif middle_name != None and last_name == None:
            full_name = first_name +" "+  middle_name  + last_name
        else :
            full_name = first_name + middle_name + last_name
        

        date_of_birth = customer_data.get("dateOfBirth")
        if "str" != type(date_of_birth).__name__:
            date_of_birth = "{:04d}-{:02d}-{:02d}".format(
                date_of_birth["year"],
                date_of_birth["monthValue"],
                date_of_birth["dayOfMonth"],
            )
        bank_accounts_info = {}
        if len(customer_data["customerBankAccounts"]) > 0:
            bank_accounts_info = customer_data["customerBankAccounts"][0]
        sm_loan_id=str(loan_data.get("id"))
        
        dedupe_data = {
                "accountNumber": bank_accounts_info.get("accountNumber"),
                "contactNumber": str(customer_data.get("mobilePhone"))[-10:],
                "customerName": full_name,
                "dateofBirth": str(date_of_birth),
                "kycDetailsList": [
                    {
                        "type": "PANCARD",
                        "value": customer_data.get("panNo")
                    },
                    {
                        "type": "AADHARCARD",
                        "value": customer_data.get("aadhaarNo")
                    }
                ],
                "loanId": str(loan_data.get("id")),
                "pincode": str(customer_data.get("pincode")),
            }
        # Posting the data to the dedupe API
        dedupe_response = await dedupe_service(dedupe_data)
        
        dedupe_data_respose_data =dedupe_response[0]
        
        
        logger.info(f'2-Success dedupe status,{dedupe_response}')
        
        is_dedupe_present = dedupe_data_respose_data.get('isDedupePresent')
        str_fetch_dedupe_info = dedupe_data_respose_data.get('dedupeReferenceId')

        if (is_dedupe_present == False):

                message_remarks = ''
                update_loan_info = await update_loan('DEDUPE', sm_loan_id, str_fetch_dedupe_info, 'Dedupe',
                                                         message_remarks,
                                                         'PROCEED', message_remarks)
                
                if(update_loan_info.status_code== 200):
                    logger.info(f"3-updated loan information with dedupe reference id to Perdix' {update_loan_info}")
                    payload['partnerHandoffIntegration']['status'] = 'SUCCESS'
                    payload['partnerHandoffIntegration']['partnerReferenceKey'] = str_fetch_dedupe_info
                else:
                    perdix_update_unsuccess = dedupe_data_respose_data(update_loan_info)
                    result = JSONResponse(status_code=500, content=perdix_update_unsuccess)
                    payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                    payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
                    logger.error(f"3a-failure fetching dedupe reference id and updating status to perdix ,{perdix_update_unsuccess}")
        else:
                dedupe_response_result = len(dedupe_data_respose_data.get('results'))
                is_eligible_flag = dedupe_data_respose_data.get('results')[dedupe_response_result-1].get('isEligible')
                message_remarks = dedupe_data_respose_data.get('results')[dedupe_response_result-1].get('message')
                if (is_eligible_flag == False):
                    update_loan_info = await update_loan('DEDUPE', sm_loan_id, str_fetch_dedupe_info, 'Rejected',
                                                         message_remarks,
                                                         'PROCEED', message_remarks)

                    if (update_loan_info.status_code == 200):
                        logger.info(f"4-updated loan information with dedupe reference to Perdix' {update_loan_info}")
                        payload['partnerHandoffIntegration']['status'] = 'SUCCESS'
                        payload['partnerHandoffIntegration']['partnerReferenceKey'] = str_fetch_dedupe_info
                    else:
                        perdix_update_unsuccess = dedupe_data_respose_data(update_loan_info)
                        result = JSONResponse(status_code=500, content=perdix_update_unsuccess)
                        payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                        payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
                        logger.error(f"4a-update unsuccess Perdix, {perdix_update_unsuccess}")
                else:
                    update_loan_info = await update_loan('DEDUPE', sm_loan_id, str_fetch_dedupe_info, 'Dedupe',
                                                         message_remarks,
                                                         'PROCEED', message_remarks)
                    if (update_loan_info.status_code == 200):
                        
                        payload['partnerHandoffIntegration']['status'] = 'SUCCESS'
                        payload['partnerHandoffIntegration']['partnerReferenceKey'] = str_fetch_dedupe_info
                    else:
                        perdix_update_unsuccess = dedupe_data_respose_data(update_loan_info)
                        result = JSONResponse(status_code=500, content=perdix_update_unsuccess)
                        payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                        payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
                        

        result = payload

        # else:
        #     dedupe_response_body_message = dedupe_data_respose_data['results']['message']
           
        #     update_loan_info = await update_loan('DEDUPE', sm_loan_id, '', 'Rejected',
        #                                          str(dedupe_response_body_message),
        #                                          'PROCEED', str(dedupe_response_body_message))
        if (update_loan_info.status_code == 200):
                
                payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
                logger.error(f"5-updated loan information for failure status, {update_loan_info}")
        else:
                perdix_update_unsuccess = dedupe_data_respose_data(update_loan_info)
                result = JSONResponse(status_code=500, content=perdix_update_unsuccess)
                payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
            
        logger.error(f"5a-post_automator_data - 174 - {dedupe_data_respose_data}")
        result = payload

    except Exception as e:
        logger.exception(f"Issue with post_automator_data function, {e.args[0]}")
        result = JSONResponse(status_code=500, content={"message": f"Issue with post_automator_data function, {e.args[0]}"})
    return result
        
       
        

        