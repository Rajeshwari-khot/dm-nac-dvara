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
import dm_nac_service.routes.sanction as sanction_route
from dm_nac_service.services.sanction import find_loan_id_from_sanction
from dm_nac_service.services.dedupe import dedupe_service
from dm_nac_service.services.sanction import find_sanction

async def fetch_data_from_db(table):
    try:
        database = get_database()
        query = table.select()
        record_array = await database.fetch_all(query)
        return record_array
    except Exception as e:
        logger.exception(f"Exception inside fetch_data_from_db from generics {e.args[0]}")


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



async def post_sanction_automator_data_service(
    
   payload

):
    """Function to prepare user data from perdix automator """
    """post into create_dedpue function"""
    """update response back to the perdix using update_loan function"""
    try:
        
        
        print("coming here")
        # Data Preparation to post the data to NAC sanction endpoint

        # customer Data
        customer_data = payload["enrollmentDTO"]["customer"]
        father_first_name = customer_data.get("fatherFirstName")
        father_middle_name = customer_data.get("fatherMiddleName")
        father_last_name = customer_data.get("fatherLastName")
        father_first_name = father_first_name if father_first_name else ""
        father_last_name = father_last_name if father_last_name else ""
        father_middle_name = father_middle_name if father_middle_name else ""
        father_full_name = father_first_name + father_middle_name + father_last_name
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
       
        income_info = {}
        if len(customer_data["familyMembers"]) > 0:
            income_info = customer_data["familyMembers"][0]["incomes"][0]
        

        emi_info = {}
        if len(customer_data["liabilities"]) > 0:
            emi_info = customer_data["liabilities"][0]
        

        repayment_info = {}
        if len(customer_data["verifications"]) > 0:
            repayment_info = customer_data["verifications"][0]

       

        # Loan Data
        loan_data = payload["loanDTO"]["loanAccount"]
        sm_loan_id = loan_data.get("id")
       
        installment_info = {}
        if len(loan_data["disbursementSchedules"]) > 0:
            installment_info = loan_data["disbursementSchedules"][0]
        
       

        schedule_date = loan_data.get("scheduleStartDate")
        if "str" != type(schedule_date).__name__:
            schedule_date = "{:04d}-{:02d}-{:02d}".format(
                schedule_date["year"],
                schedule_date["monthValue"],
                schedule_date["dayOfMonth"],
            )

        frequency = loan_data.get("frequency")
        if(frequency == 'M'):
            
            repayment_frequency = 'WEEKLY'
            tenure_unit = 'MONTHS'
        if(frequency == 'W'):
            repayment_frequency = 'WEEKLY'
            tenure_unit = 'WEEKS'
        if (frequency == 'D'):
            repayment_frequency = 'DAILY'
            tenure_unit = 'DAYS'
        if (frequency == 'Y'):
            tenure_unit = 'YEARS'
        if (frequency == 'F'):
            repayment_frequency = 'FORTNIGHTLY'

        sanction_data = {
                "mobile": str(customer_data.get("mobilePhone"))[-10:],
                "firstName": customer_data.get("firstName"),
                "lastName": customer_data.get("lastName"),
                "fatherName": father_full_name,
                "gender": customer_data.get('gender'),
                "idProofTypeFromPartner": "PANCARD",
                "idProofNumberFromPartner": customer_data.get("panNo"),
                "addressProofTypeFromPartner": "AADHARCARD",
                "addressProofNumberFromPartner": customer_data.get("aadhaarNo"),
                "dob": str(date_of_birth),
                "ownedVehicle": customer_data.get("vehiclesOwned"),
                "currDoorAndBuilding": customer_data.get("doorNo"),
                "currStreetAndLocality":customer_data.get("mailingLocality"),
                "currLandmark": customer_data.get("landmark"),
                "currCity": customer_data.get("mailingLocality"),
                "currDistrict": customer_data.get("district"),
                "currState": customer_data.get("state"),
                "currPincode": str(customer_data.get("pincode")),
                "permDoorAndBuilding": customer_data.get("doorNo"),
                "permLandmark": customer_data.get("landmark"),
                "permCity":customer_data.get("locality"),
                "permDistrict": customer_data.get("district"),
                "permState": customer_data.get("state"),
                "permPincode": str(customer_data.get("pincode")),
                "companyName": customer_data['udf']['userDefinedFieldValues']['udf7'],
                "clientId": str(loan_data.get("customerId")),
                "grossMonthlyIncome": income_info.get("incomeEarned"),
                "netMonthlyIncome": income_info.get("incomeEarned"),
                "pan": customer_data.get("panNo"),
                "purposeOfLoan":customer_data.get("requestedLoanPurpose") ,
                "loanAmount":loan_data.get("loanAmount") ,
                "interestRate":loan_data.get("interestRate") ,
                "scheduleStartDate": schedule_date,
                "firstInstallmentDate": installment_info.get("firstRepaymentDate"),
                "totalProcessingFees": loan_data.get("processingFeeInPaisa"),
                "preEmiAmount": loan_data.get("preEmi"),
                "emi": loan_data.get("emi"),
                "emiDate": emi_info.get("emiDate"),
                "repaymentFrequency": repayment_frequency,
                "repaymentMode": repayment_info.get("modeOfPayment"),
                "tenureValue": int(loan_data.get("tenure")),
                "tenureUnits": tenure_unit,
                "productName": loan_data.get("productCode"),
                "primaryBankAccount": bank_accounts_info.get("accountNumber"),
                "bankName":  bank_accounts_info.get("customerBankName"),
                "email": customer_data.get("email"),
                "dedupeReferenceId":5164099725015263,
                "middleName": customer_data.get("middleName"),
                "maritalStatus": customer_data.get("maritalStatus"),
                "loanId": str(sm_loan_id),
                }
        
        sanction_data['emiWeek'] = 1
        sanction_data['modeOfSalary'] = "ONLINE"
        sanction_data['incomeValidationStatus'] = "SUCCESS"
        # sanction_data['dedupeReferenceId']=5162049357311508,
        sanction_data['gst'] = 0
        sanction_data['occupation']="SALARIED_OTHER"

        logger.info(f'1 -Sanction Data from Perdix and Sending the data to create sanction function {sanction_data}')
        sanction_response = await sanction_route.sanction_service(sanction_data)
        print("SANCTION",sanction_response.status_code)
        sanction_response_perdix_dict = generics.response_to_dict(sanction_response)
        print(sanction_response,sanction_response_perdix_dict) 
        # sanction_response_dict=
        sanction_response_status = generics.hanlde_response_status(sanction_response)
        # print("dict",sanction_response_status)
        sanction_response_body = generics.hanlde_response_body(sanction_response)
        # print("BODY",sanction_response_body)

        
        if(sanction_response.status_code == 200):

            get_sanction_ref = await find_sanction(sm_loan_id)
            get_sanction_ref_status = generics.hanlde_response_status(get_sanction_ref)
            response_body_json = generics.hanlde_response_body(get_sanction_ref)
            if(get_sanction_ref_status == 200):
                reference_id = str(response_body_json.get('customerId'))
                message_remarks = 'Customer Created Successfully'

                # To Update Perdix with Sanction Reference ID
                update_loan_info = await update_loan('SANCTION', sm_loan_id, reference_id, 'Dedupe', message_remarks,
                                                     'PROCEED', message_remarks)
                update_loan_info_status = generics.hanlde_response_status(update_loan_info)
                if(update_loan_info_status == 200):
                    logger.info(f"7-updated loan info with customer_id,{update_loan_info}")    
                    payload['partnerHandoffIntegration']['status'] = 'SUCCESS'
                    payload['partnerHandoffIntegration']['partnerReferenceKey'] = reference_id
                    result = payload
                else:
                    loan_update_error = generics.hanlde_response_body(get_sanction_ref)
                    logger.error(f"failure fecthing customer_id - 350 - {loan_update_error}")
                    result = JSONResponse(status_code=500, content=loan_update_error)
                    payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                    payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
                    result = payload
            else:
                logger.error(f"post_sanction_automator_data - 356 - {response_body_json}")
                result = JSONResponse(status_code=500, content=response_body_json)
                payload['partnerHandoffIntegration']['status'] = 'FAILURE'
                payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
                result = payload
        else:
           
            sanction_response_get_body = sanction_response_body.get('body')
            sanction_response_get_body_json = json.loads(sanction_response_get_body)
            sanction_response_get_body_value = sanction_response_get_body_json.get('content').get('value')
            update_loan_info = await update_loan('SANCTION', sm_loan_id, '', 'Rejected', str(sanction_response_get_body_value),
                                                 'PROCEED', str(sanction_response_get_body_value))
            logger.error(f"post_sanction_automator_data - 368,{sanction_response_body}")
            result = JSONResponse(status_code=500, content=sanction_response_body)
            payload['partnerHandoffIntegration']['status'] = 'FAILURE'
            payload['partnerHandoffIntegration']['partnerReferenceKey'] = ''
            result = payload
    except Exception as e:
        logger.exception(f"Issue with post_sanction_automator_data function, {e.args[0]}")
        result = JSONResponse(status_code=500,content={"message": f"Issue with post_automator_data function, {e.args[0]}"})
    return result


async def update_sanction_services():
    try:
        database = get_database()
        database_record_fetch = await fetch_data_from_db(sanction)
        
        for i in database_record_fetch:
            customer_id = i[1]
            sm_loan_id = i[61]
            sanction_gt_response = await nac_gateway.nac_sanction(customer_id)
            
            sanction_gt_response_status = generics.hanlde_response_status(sanction_gt_response)
            sanction_gt_response_body = generics.hanlde_response_body(sanction_gt_response)
            
            if(sanction_gt_response_status == 200):
                logger.info(f"1-getting response from nac', {sanction_gt_response_body}")
                sanction_status = sanction_gt_response_body.get('content').get('status')
               
                if (sanction_status == 'SUCCESS'):
                    
                    sanction_status_value = sanction_gt_response_body['content']['value']
                    sanction_status_value_status = sanction_gt_response_body['content']['value']['status']
                    if (sanction_status_value_status == 'ELIGIBLE'):
                       
                        sanction_status_value_reference_id = sanction_gt_response_body['content']['value'][
                            'sanctionReferenceId']
                        sanction_status_value_bureau_fetch = sanction_gt_response_body['content']['value'][
                            'bureauFetchStatus']
                        
                        query = sanction.update().where(sanction.c.customer_id == customer_id).values(
                            status=sanction_status_value_status,
                           
                            sanctin_ref_id=sanction_status_value_reference_id,
                            bureau_fetch_status=sanction_status_value_bureau_fetch)
                        sanction_updated = await database.execute(query)
                        update_loan_info = await update_loan('SANCTION-REFERENCE', sm_loan_id,
                                                             sanction_status_value_reference_id, 'Dedupe',
                                                             sanction_status_value_bureau_fetch,
                                                             'PROCEED', sanction_status_value_bureau_fetch)
                    elif (sanction_status_value_status == 'REJECTED'):
                        
                        sanction_status_value_stage = sanction_gt_response_body['content']['value'][
                            'stage']
                        sanction_status_value_bureau_fetch = sanction_gt_response_body['content']['value'][
                            'bureauFetchStatus']
                        if (sanction_status_value_stage == 'BUREAU_FETCH'):
                           

                            query = sanction.update().where(sanction.c.customer_id == customer_id).values(
                                status=sanction_status_value_status,
                                stage=sanction_status_value_stage,
                                bureau_fetch_status=sanction_status_value_bureau_fetch)
                            sanction_updated = await database.execute(query)
                            update_loan_info = await update_loan('SANCTION', sm_loan_id, '',
                                                                 'Rejected',
                                                                 sanction_status_value_bureau_fetch,
                                                                 'PROCEED', sanction_status_value_bureau_fetch)
                        else:
                            
                            sanction_status_value_reject_reason = str(sanction_gt_response_body['content']['value'][
                                                                          'rejectReason'])
                            
                            query = sanction.update().where(sanction.c.customer_id == customer_id).values(
                                status=sanction_status_value_status,
                                stage=sanction_status_value_stage,
                                reject_reason=sanction_status_value_reject_reason,
                                bureau_fetch_status=sanction_status_value_bureau_fetch)
                            sanction_updated = await database.execute(query)
                            update_loan_info = await update_loan('SANCTION', sm_loan_id, '',
                                                                 'Rejected',
                                                                 sanction_status_value_reject_reason,
                                                                 'PROCEED', sanction_status_value_reject_reason)
                    else:
                        sanction_status_value_stage = sanction_gt_response_body['content']['value'][
                            'stage']
                        sanction_status_value_bureau_fetch = sanction_gt_response_body['content']['value'][
                            'bureauFetchStatus']
                        query = sanction.update().where(sanction.c.customer_id == customer_id).values(
                            status=sanction_status_value_status,
                            stage=sanction_status_value_stage,
                            
                            bureau_fetch_status=sanction_status_value_bureau_fetch)
                        sanction_updated = await database.execute(query)
                        update_loan_info = await update_loan('SANCTION', sm_loan_id, '',
                                                             'Dedupe',
                                                             sanction_status_value_bureau_fetch,
                                                             'PROCEED', sanction_status_value_bureau_fetch)
                else:
                    logger.error(f" Error from Northern Arc-681 {sanction_gt_response_body}")
                    result = JSONResponse(status_code=500, content=sanction_gt_response_body)

            else:
                logger.error(f" Error from Northern Arc-685 {sanction_gt_response_body}")
                result = JSONResponse(status_code=500, content=sanction_gt_response_body)

        return database_record_fetch
    except Exception as e:
        logger.exception(f"Issue with update_sanction_in_db function, {e.args[0]}")
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
        return result

        
       
        

        