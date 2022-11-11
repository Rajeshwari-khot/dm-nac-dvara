from email import message
from http import client
from fastapi.responses import JSONResponse
from dm_nac_service.config.database import get_database
from dm_nac_service.models.sanction import sanction
from dm_nac_service.models.sanction import sanction_fileupload
import dm_nac_service.models.sanction as sanction_model
from dm_nac_service.resource.logging_config import logger



async def insert(sanction_object,payload):
    try:       
        sanction_message=sanction_object.get('content').get('message')
        sanction_status=sanction_object.get('content').get('status')
        sanction_customer_id=sanction_object.get('content').get('value').get('customerId')
        sanction_client_id=sanction_object.get('content').get('value').get('clientId')
        sanction_dedupe_refrence_id=payload.get('dedupeReferenceId')
        sanction_loan_id=payload.get("loanId")
        sanction_mobile=payload.get("mobile")
        sanction_first_name=payload.get("firstName")
        sanction_last_name=payload.get("lastName")
        sanction_father_name=payload.get("fatherName")
        sanction_gender=payload.get("gender")
        sanction_id_proof_type=payload.get("idProofTypeFromPartner")
        sanction_id_proof_number_type=payload.get("idProofNumberFromPartner")
        sanction_address_proof_type=payload.get("addressProofTypeFromPartner")
        sanction_address_proof_number_type=payload.get("addressProofNumberFromPartner")
        sanction_dob=payload.get("dob")
        sanction_owned_vehicle=payload.get("ownedVehicle")
        sanction_curr_door=payload.get("currDoorAndBuilding")
        sanction_curr_street=payload.get("currStreetAndLocality")
        sanction_curr_landmark=payload.get("currLandmark")
        sanction_curr_city=payload.get("currCity")
        sanction_curr_district=payload.get("currDistrict")
        sanction_curr_state=payload.get("currState")
        sanction_curr_pincode=payload.get("currPincode")
        sanction_perm_door=payload.get("permDoorAndBuilding")
        sanction_perm_landmark=payload.get("permLandmark")
        sanction_perm_city=payload.get("permCity")
        sanction_perm_district=payload.get("permDistrict")
        sanction_perm_state=payload.get("permState")
        sanction_perm_pincode=payload.get("permPincode")
        sanction_company_name=payload.get("companyName")
        sanction_gross_income=payload.get("grossMonthlyIncome")
        sanction_net_income=payload.get("netMonthlyIncome")
        sanction_pan=payload.get("pan")
        sanction_purpose_of_loan=payload.get("purposeOfLoan")
        sanction_loan_amount=payload.get("loanAmount")
        sanction_interest_rate=payload.get("interestRate")
        sanction_schedule_start_date=payload.get("scheduleStartDate")
        sanction_first_installment_date=payload.get("firstInstallmentDate")
        sanction_total_processing_fee=payload.get("totalProcessingFees")
        sanction_pre_emi=payload.get("preEmiAmount")
        sanction_emi=payload.get("emi")
        sanction_emi_date=payload.get("emiDate")
        sanction_repayment_frequency=payload.get("repaymentFrequency")
        sanction_repayment_mode=payload.get("repaymentMode")
        sanction_tenure_value=payload.get("tenureValue")
        sanction_tenure_units=payload.get("tenureUnits")
        sanction_product_name=payload.get("productName")
        sanction_primary_bank_account=payload.get("primaryBankAccount")
        sanction_bank_name=payload.get("bankName")
        sanction_email=payload.get("email")
        sanction_middle_name=payload.get("middleName")
        sanction_maritual_status=payload.get("maritalStatus")
        sanction_emi_week=payload.get("emiWeek")
        sanction_mode_of_salary=payload.get("modeOfSalary")
        sanction_income_validation_status=payload.get("incomeValidationStatus")
        sanction_gst=payload.get("gst")
        sanction_occupation=payload.get("occupation")
        database = get_database()
        query = sanction.insert().values(message=sanction_message,
                                            sanction_status=sanction_status,
                                            customer_id=str(sanction_customer_id),
                                            loan_id=sanction_loan_id,
                                            client_id=sanction_client_id,
                                            dedupe_reference_id=sanction_dedupe_refrence_id,
                                            mobile=sanction_mobile,
                                            first_name=sanction_first_name,
                                            last_name=sanction_last_name,
                                            father_name=sanction_father_name,
                                            gender=sanction_gender,
                                            id_proof_type_from_partner=sanction_id_proof_type,
                                            id_proof_number_from_partner=sanction_id_proof_number_type,
                                            address_proof_type_from_partner=sanction_address_proof_type,
                                            address_proof_number_from_partner=sanction_address_proof_number_type,
                                            dob=sanction_dob,
                                            owned_vehicle=sanction_owned_vehicle,
                                            curr_door_and_building=sanction_curr_door,
                                            curr_street_and_locality=sanction_curr_street,
                                            curr_landmark=sanction_curr_landmark,
                                            curr_city=sanction_curr_city,
                                            curr_district=sanction_curr_district,
                                            curr_state=sanction_curr_state,
                                            curr_pincode=sanction_curr_pincode,
                                            perm_door_and_building=sanction_perm_door,
                                            perm_landmark=sanction_perm_landmark,
                                            perm_city=sanction_perm_city,
                                            perm_district=sanction_perm_district,
                                            perm_state=sanction_perm_state,
                                            perm_pincode=sanction_perm_pincode,
                                            company_name=sanction_company_name,
                                            gross_monthly_income=sanction_gross_income,
                                            net_monthly_income=sanction_net_income,
                                            income_validation_status=sanction_income_validation_status,
                                            pan=sanction_pan,
                                            purpose_of_loan=sanction_purpose_of_loan,
                                            loan_amount=sanction_loan_amount,
                                            interest_rate=sanction_interest_rate,
                                            schedule_start_date=sanction_schedule_start_date,
                                            first_installment_date=sanction_first_installment_date,
                                            total_processing_fees=sanction_total_processing_fee,
                                            gst=sanction_gst,
                                            pre_emi_amount=sanction_pre_emi,
                                            emi=sanction_emi,
                                            emi_date=sanction_emi_date,
                                            emi_week=sanction_emi_week,
                                            repayment_frequency=sanction_repayment_frequency,
                                            repayment_mode=sanction_repayment_mode,
                                            tenure_value=sanction_tenure_value,
                                            tenure_units=sanction_tenure_units,
                                            product_name=sanction_product_name,
                                            primary_bank_account=sanction_primary_bank_account,
                                            bank_name=sanction_bank_name,
                                            mode_of_salary=sanction_mode_of_salary,
                                            email=sanction_email,
                                            middle_name=sanction_middle_name,
                                            marital_status=sanction_maritual_status,
                                            occupation=sanction_occupation
                                              )
        await database.execute(query)
        logger.info(f"sanction  INFO LOG SUCCESSFULLY INSERTED INTO SANCTION TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY - SANCTION - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})

async def insert_file_reponse(sanction_file_upload_object):
    try:
        print("sanction_file_upload_object",sanction_file_upload_object)
        sanction_file_upload_message=sanction_file_upload_object.get('content').get('message')
        sanction_file_upload_status=sanction_file_upload_object.get('content').get('status')
        
        database = get_database()
        query = sanction_fileupload.insert().values(message=sanction_file_upload_message,
                                         status=sanction_file_upload_status
        )
        await database.execute(query)
        logger.info(f"FILE_UPLOAD  INFO LOG SUCCESSFULLY INSERTED INTO SANCTION TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY - FILE_UPLOAD - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



async def insert_get_sanction_status(customer_id,sanction_status_object):
    try:
        
        sanction_get_status=sanction_status_object.get('content').get('status')
        sanction_get_value_status=sanction_status_object.get('content').get('value').get('status')
        sanction_get_stage=sanction_status_object.get('content').get('value').get('stage')
        sanction_get_sanction_reference_id=sanction_status_object.get('content').get('value').get('sanctionReferenceId') 
        sanction_get_bureau_fetch_status=sanction_status_object.get('content').get('value').get('bureauFetchStatus')
        sanction_get_reject_reason=sanction_status_object.get('content').get('value').get('rejectReason')
        
        database = get_database()
        query = sanction_model.sanction.update().where(sanction.c.customer_id==customer_id).values(status=sanction_get_status,
                                         value_status=sanction_get_value_status,
                                         stage=sanction_get_stage,
                                         sanction_reference_id=sanction_get_sanction_reference_id,
                                         bureau_fetch_status=sanction_get_bureau_fetch_status,
                                         reject_reason=sanction_get_reject_reason

        )
        await database.execute(query)
        logger.info(f"GET SANCTION STATUS  INFO LOG SUCCESSFULLY INSERTED INTO SANCTION TABLE")
    except Exception as e:
        logger.exception(f"REPOSITORY - SANCTION- STATUS - INSERT - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})



        # sanction_mobile=sanction_object.get('mobile')
        # sanction_first_name=sanction_object.get('first_name')
        # sanction_last_name=sanction_object.get('last_name')
        # sanction_father_name=sanction_object.get('father_name')
        # sanction_gender=sanction_object.get('gender')
        # sanction_id_proof_type_from_partner=sanction_object.get('id_proof_type_from_partner')
        # sanction_id_proof_number_from_partner=sanction_object.get('id_proof_number_from_partner')
        # sanction_address_proof_type_from_partner=sanction_object.get('address_proof_type_from_partner')
        # sanction_address_proof_number_from_partner=sanction_object.get('address_proof_number_from_partner')
        # sanction_dob=sanction_object.get('dob')
        # sanction_owned_vehicle=sanction_object.get('owned_vehicle')
        # sanction_curr_door_and_building=sanction_object.get('curr_door_and_building')
        # sanction_curr_street_and_locality=sanction_object.get('curr_street_and_locality')
        # sanction_curr_landmark=sanction_object.get('curr_landmark')
        # sanction_curr_city=sanction_object.get('curr_city')
        # sanction_curr_district=sanction_object.get('curr_district')
        # sanction_curr_state=sanction_object.get('curr_state')
        # sanction_curr_pincode=sanction_object.get('curr_pincode')
        # sanction_perm_door_and_building=sanction_object.get('perm_door_and_building')
        # sanction_perm_landmark=sanction_object.get('perm_landmark')
        # sanction_perm_city=sanction_object.get('perm_city')
        # sanction_perm_district=sanction_object.get('perm_district')
        # sanction_perm_state=sanction_object.get('perm_state')
        # sanction_perm_pincode=sanction_object.get('')
        # sanction_occupation=sanction_object.get('occupation')
        # sanction_company_name=sanction_object.get('company_name')
        # sanction_gross_monthly_income=sanction_object.get('gross_monthly_income')
        # sanction_net_monthly_income=sanction_object.get('net_monthly_income')
        # sanction_income_validation_status=sanction_object.get('income_validation_status')
        # sanction_pan=sanction_object.get('pan')
        # sanction_purpose_of_loan=sanction_object.get('purpose_of_loan')
        # sanction_loan_amount=sanction_object.get('loan_amount')
        # sanction_interest_rate=sanction_object.get('interest_rate')
        # sanction_schedule_start_date=sanction_object.get('schedule_start_date')
        # sanction_first_installment_date=sanction_object.get('first_installment_date')
        # sanction_total_processing_fees=sanction_object.get('total_processing_fees')
        # sanction_gst=sanction_object.get('gst')
        # sanction_pre_emi_amount=sanction_object.get('pre_emi_amount')
        # sanction_emi=sanction_object.get('emi')
        # sanction_emi_date=sanction_object.get('emi_date')
        # sanction_emi_week=sanction_object.get('emi_week')
        # sanction_repayment_frequency=sanction_object.get('repayment_frequency')
        # sanction_repayment_mode=sanction_object.get('repayment_mode')
        # sanction_tenure_value=sanction_object.get('tenure_value')
        # sanction_tenure_units=sanction_object.get('tenure_units')
        # sanction_product_name=sanction_object.get('product_name')
        # sanction_primary_bank_account=sanction_object.get('primary_bank_account')
        # sanction_bank_name=sanction_object.get('bank_name')
        # sanction_mode_of_salary=sanction_object.get('mode_of_salary')
        # sanction_client_id=sanction_object.get('client_id')
        # sanction_dedupe_reference_id=sanction_object.get('dedupe_reference_id')
        # sanction_email=sanction_object.get('email')
        # sanction_middle_name=sanction_object.get('middle_name')
        # sanction_marital_status=sanction_object.get('marital_status')
        # sanction_loan_id=sanction_object.get('loan_id')
        # sanction_created_date=sanction_object.get('created_date')
        # sanction_updated_date=sanction_object.get('updated_date')
        















