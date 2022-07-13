import json
from datetime import datetime
from fastapi import APIRouter, Depends, status, Request, Response, Body
from fastapi.responses import JSONResponse
from dm_nac_service.routes.dedupe import create_dedupe, find_dedupe
from dm_nac_service.data.database import get_database, sqlalchemy_engine, insert_logs
from dm_nac_service.gateway.nac_perdix_automator import perdix_post_login, perdix_fetch_loan, perdix_update_loan
from dm_nac_service.gateway.nac_sanction import nac_sanction
from dm_nac_service.routes.sanction import create_sanction
from dm_nac_service.resource.generics import response_to_dict

router = APIRouter()


@router.post("/nac-dedupe-automator-data", status_code=status.HTTP_200_OK, tags=["Automator"])
async def post_automator_data(
    # request_info: Request,
    # response: Response

    # Below is to test manually by providing json data in request body
    request_info: dict = Body(...),

):
    """Function which prepares user data and posts"""
    try:
        print('*********************************** DATA FROM PERDIX THROUGH AUTOMATOR ***********************************')
        # payload = await request_info.json()

        # Below is for data published manually
        payload = request_info
        # print('data from post automator data', payload)

        customer_data = payload["enrollmentDTO"]["customer"]
        loan_data = payload["loanDTO"]["loanAccount"]
        first_name = customer_data.get("firstName", "")
        middle_name = customer_data.get("", "Dummy")
        last_name = customer_data.get("", "Dummy")
        first_name = first_name if first_name else ""
        last_name = last_name if last_name else ""
        middle_name = middle_name if middle_name else ""
        full_name = f"{first_name} {middle_name} {last_name}"
        date_of_birth = customer_data.get("dateOfBirth", "")
        if "str" != type(date_of_birth).__name__:
            date_of_birth = "{:04d}-{:02d}-{:02d}".format(
                date_of_birth["year"],
                date_of_birth["monthValue"],
                date_of_birth["dayOfMonth"],
            )
        mobile_number = str(customer_data.get("mobilePhone", "9862590000"))[-10:]
        pincode = str(customer_data.get("pincode", ""))
        sm_loan_id = loan_data.get("id", "SML00253011")
        udhyog_aadhar = customer_data.get("aadhaarNo")
        pan_no = customer_data.get("panNo", "ALWPG5909L")
        bank_accounts_info = {}
        if len(customer_data["customerBankAccounts"]) > 0:
            bank_accounts_info = customer_data["customerBankAccounts"][0]
        account_number = bank_accounts_info.get("accountNumber", "00301530887")
        dedupe_data = {
                "accountNumber": account_number,
                "contactNumber": mobile_number,
                "customerName": full_name,
                "dateofBirth": str(date_of_birth),
                "kycDetailsList": [
                    {
                        "type": "PANCARD",
                        "value": pan_no
                    },
                    {
                        "type": "AADHARCARD",
                        "value": udhyog_aadhar
                    }
                ],
                "loanId": str(sm_loan_id),
                "pincode": pincode,
            }

        print('1 - prepared data from automator function', dedupe_data)

        # Posting the data to the dedupe API
        dedupe_response = await create_dedupe(dedupe_data)
        print('12 - coming back to automator function', dedupe_response)

        # Fetch loan id from DB
        fetch_dedupe_info = await find_dedupe(sm_loan_id)
        print('13 - extracting loan information from Perdix', fetch_dedupe_info)

        # Condition to check the success and failure case
        sm_loan_id = 287
        is_eligible_flag = fetch_dedupe_info.get('isEligible', '')
        str_fetch_dedupe_info = fetch_dedupe_info.get('dedupeRefId', '')
        message_remarks = fetch_dedupe_info.get('message', '')
        print('priting dedupe reference id ', str_fetch_dedupe_info)
        if(is_eligible_flag == ''):
            print('is eligible none', is_eligible_flag)
            update_loan_info = await update_loan(sm_loan_id, str_fetch_dedupe_info, 'Dedupe', message_remarks,
                                                 'PROCEED', message_remarks)
            print('14 - updated loan information with dedupe reference to Perdix', update_loan_info)
        else:
            print('is eligible not none', is_eligible_flag)
            update_loan_info = await update_loan(sm_loan_id, str_fetch_dedupe_info, 'Rejected', message_remarks,
                                                 'PROCEED', message_remarks)
            print('14 - updated loan information with dedupe reference to Perdix', update_loan_info)
        # Posting the loan id to the Perdix API
        # Fake loan id
        sm_loan_id = 287
        # fetch_loan_info = await perdix_fetch_loan(sm_loan_id)
        # print('13 - extracting loan information from Perdix', fetch_loan_info)

        # Updating Dedupe Reference ID to Perdix API
        # str_fetch_dedupe_info = str(fetch_dedupe_info)



        return dedupe_data
    except Exception as e:
        print(e)
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Issue with Northern Arc API, {e.args[0]}"})




@router.post("/nac-sanction-automator-data", status_code=status.HTTP_200_OK, tags=["Automator"])
async def post_sanction_automator_data(
    # request_info: Request,
    # response: Response
    # Below is to test manually by providing json data in request body
    request_info: dict = Body(...),
):
    """Function which prepares user data and posts"""
    try:
        # print("coming inside prepare sanction data")
        # payload = await request_info.json()

        # Below is for data published manually
        payload = request_info

        # Get Dedupe Reference ID
        # sm_loan_id = 287
        # print('before loan fetch')
        # fetch_dedupe_info = await find_dedupe(sm_loan_id)
        dedupe_reference_id = "5134610851082868"
        # print(fetch_dedupe_info)


        customer_data = payload["enrollmentDTO"]["customer"]
        loan_data = payload["loanDTO"]["loanAccount"]
        first_name = customer_data.get("firstName", "")
        middle_name = customer_data.get("", "Dummy")
        last_name = customer_data.get("", "Dummy")
        first_name = first_name if first_name else ""
        last_name = last_name if last_name else ""
        middle_name = middle_name if middle_name else ""
        full_name = f"{first_name} {middle_name} {last_name}"
        gender = payload.get("gender", "")
        gender = "MALE" if gender == "MALE" else "FEMALE"
        father_first_name = customer_data.get("fatherFirstName", "")
        father_middle_name = customer_data.get("fatherMiddleName", "")
        father_last_name = customer_data.get("fatherLastName", "")
        father_first_name = father_first_name if father_first_name else ""
        father_last_name = father_last_name if father_last_name else ""
        father_middle_name = father_middle_name if father_middle_name else ""
        father_full_name = father_first_name + father_middle_name + father_last_name
        date_of_birth = customer_data.get("dateOfBirth", "")
        if "str" != type(date_of_birth).__name__:
            date_of_birth = "{:04d}-{:02d}-{:02d}".format(
                date_of_birth["year"],
                date_of_birth["monthValue"],
                date_of_birth["dayOfMonth"],
            )
        mobile_number = str(customer_data.get("mobilePhone", "9862590000"))[-10:]
        pincode = str(customer_data.get("pincode", ""))
        sm_loan_id = loan_data.get("id", "SML00253011")
        udhyog_aadhar = customer_data.get("aadhaarNo")
        pan_no = customer_data.get("panNo", "ALWPG5909L")
        bank_accounts_info = {}
        if len(customer_data["customerBankAccounts"]) > 0:
            bank_accounts_info = customer_data["customerBankAccounts"][0]
        account_number = bank_accounts_info.get("accountNumber", "1234313323")
        customer_bank_name = bank_accounts_info.get("customerBankName", "YES BANK LIMITED")
        owned_vehicle = customer_data.get("","2W")
        curr_door_number = customer_data.get("doorNo", "jayanagar201")
        curr_locality = customer_data.get("locality", "bangalore")
        landmark = customer_data.get("","banashankari circle")
        curr_district = customer_data.get("district","bangalore")
        # curr_city=customer_data.get("","bangalore")
        curr_state = customer_data.get("state","Karnataka")
        occupation_info = {}
        if len(customer_data["familyMembers"]) > 0:
            occupation_info = customer_data["familyMembers"][0]
        curr_occupation = occupation_info.get("occupation", "SALARIED_OTHER")
        mode_salary = occupation_info.get("", "ONLINE")
        installment_info = {}
        if len(loan_data["disbursementSchedules"]) > 0:
            installment_info = loan_data["disbursementSchedules"][0]
        installment_date = installment_info.get("", "2020-04-11")
        income_info = {}
        if len(customer_data["familyMembers"]) > 0:
            income_info = customer_data["familyMembers"][0]["incomes"][0]
        gross_income = income_info.get("incomeEarned", 30000)
        net_income = income_info.get("incomeEarned", 40000)
        loan_purpose = loan_data.get("requestedLoanPurpose","Others-TO BUY GOLD")
        loan_amount = loan_data.get("loanAmount","10000")
        interest_rate = loan_data.get("interestRate","25")
        schedule_date = loan_data.get("scheduleStartDate", "")
        if "str" != type(schedule_date).__name__:
            schedule_date = "{:04d}-{:02d}-{:02d}".format(
                schedule_date["year"],
                schedule_date["monthValue"],
                schedule_date["dayOfMonth"],
            )
        process_fee = loan_data.get("processingFeeInPaisa", 900)
        pre_emi = loan_data.get("", 0)
        max_emi = loan_data.get("emi", 100)
        gst = loan_data.get("",0)
        emi_info = {}
        if len(customer_data["liabilities"]) > 0:
            emi_info = customer_data["liabilities"][0]
        emi_date = emi_info.get("", "2022-04-10")
        repayment_frequency = payload.get("frequency", "WEEKLY")
        repayment_frequency = "Monthly" if repayment_frequency == "Monthly" else "F"
        repayment_frequency = loan_data.get("frequencyRequested","WEEKLY")
        tenure_value = loan_data.get("tenure", 36)
        product_name = loan_data.get("productCode", "Personal Loan")
        email_id = customer_data.get("email", "testsm1@gmail.com")
        maritual_status = customer_data.get("maritalStatus", "MARRIED")
        client_id = loan_data.get("customerId", "12345")
        repayment_info = {}
        if len(customer_data["verifications"]) > 0:
            repayment_info = customer_data["verifications"][0]
        repayment_mode = repayment_info.get("", "NACH")
        sanction_data = {
                "mobile": mobile_number,
                "firstName": first_name,
                "lastName": last_name,
                "fatherName": father_full_name,
                "gender": gender,
                "idProofTypeFromPartner": "PANCARD",
                "idProofNumberFromPartner": pan_no,
                "addressProofTypeFromPartner": "AADHARCARD",
                "addressProofNumberFromPartner": udhyog_aadhar,
                "dob": str(date_of_birth),
                "ownedVehicle": owned_vehicle,
                "currDoorAndBuilding": curr_door_number,
                "currStreetAndLocality":curr_locality,
                "currLandmark": landmark,
                "currCity": "",
                "currDistrict": curr_district,
                "currState": curr_state,
                "currPincode": pincode,
                "permDoorAndBuilding": curr_door_number,
                "permLandmark": landmark,
                "permCity":"",
                "permDistrict": curr_district,
                "permState": curr_state,
                "permPincode": pincode,
                "occupation": curr_occupation,
                "companyName": "",
                "clientId": str(client_id),
                "grossMonthlyIncome": gross_income,
                "netMonthlyIncome": net_income,
                "incomeValidationStatus": "",
                "pan": pan_no,
                "purposeOfLoan":loan_purpose ,
                "loanAmount":loan_amount ,
                "interestRate":interest_rate ,
                "scheduleStartDate": schedule_date,
                "firstInstallmentDate": installment_date,
                "totalProcessingFees": process_fee,
                "gst": gst,
                "preEmiAmount": pre_emi,
                "emi": max_emi,
                "emiDate": emi_date,
                "emiWeek": "",
                "repaymentFrequency": repayment_frequency,
                "repaymentMode": repayment_mode,
                "tenureValue": int(tenure_value),
                "tenureUnits": "",
                "productName": product_name,
                "primaryBankAccount": account_number,
                "bankName": customer_bank_name,
                "modeOfSalary": mode_salary,
                "dedupeReferenceId": dedupe_reference_id,
                "email": email_id,
                "middleName": middle_name,
                "maritalStatus": maritual_status,
                "loanId": str(sm_loan_id),
                }
        print('1 - Sanction Data from Perdix and Sending the data to create sanction function', sanction_data)
        sanction_response = await create_sanction(sanction_data)
        update_loan_info = await update_loan(sm_loan_id, str_fetch_dedupe_info, 'Dedupe', message_remarks,
                                             'PROCEED', message_remarks)
        # print('0 - testing', sanction_response)
        # print('1 - Prepare Data to push to NAC endpoint', sanction_data)
        # return sanction_data

        return sanction_data
    except Exception as e:
        print(e)



@router.get("/perdix/{loan_id}", status_code=status.HTTP_200_OK, tags=["Perdix"])
async def get_loan(loan_id):
    result = await perdix_post_login()
    # print(result)
    get_perdix_loan_data = await perdix_fetch_loan(loan_id)
    # print('getting customer', get_perdix_data)

    return get_perdix_loan_data


@router.post("/perdix/update-loan", tags=["Perdix"])
async def update_loan(

    # request_info: Request,
    # response: Response

    # For testing manually
    # loan_info: dict = Body(...),

    loan_id: int,
    dedupe_ref_id: str,
    stage: str,
    reject_reason: str,
    loan_process_action: str,
    remarks: str
):
    # result = loan_info

    #  For testing manually
    # loan_update_response = await perdix_update_loan(loan_info)
    # result = loan_update_response

    # For Real updating the loan information
    get_loan_info = await perdix_fetch_loan(loan_id)
    # print('get loan info', get_loan_info)
    # print('Reject Reason - ', get_loan_info.get('loanAccount').get('rejectReason'))
    # print('Stage - ', get_loan_info.get('stage'))
    # print('Remarks - ', get_loan_info.get('remarks'))
    # print('loanProcessAction - ', get_loan_info.get('loanProcessAction'))
    # print('udf41 - ', get_loan_info.get('accountUserDefinedFields').get('userDefinedFieldValues').get('udf41'))
    json_data_version = get_loan_info.get('version')
    # print('printing version of data ', json_data_version)
    if "rejectReason" in get_loan_info:
        get_loan_info['rejectReason'] = reject_reason
    # if "stage" in get_loan_info:
    #     get_loan_info['stage'] = "Testing stage"
    get_loan_info['stage'] = stage
    if "remarks1" in get_loan_info:
        get_loan_info['remarks1'] = "Testing remarks1"
    if "loanProcessAction" in get_loan_info:
        get_loan_info['loanProcessAction'] = "Testing loanProcessAction"
    if "accountUserDefinedFields" in get_loan_info:
        get_loan_info['accountUserDefinedFields']['userDefinedFieldValues'] = {
            'udf41': dedupe_ref_id
            # 'udf42': "5211201547885960"
            # 'udf43': "5211201547885960"
            # 'udf44': "5211201547885960"
            # 'udf45': "5211201547885960"
        }
    # if "version" in get_loan_info:
    #     get_loan_info['version'] = json_data_version + 2

    prepare_loan_info = {
        "loanAccount": get_loan_info,
        "loanProcessAction": loan_process_action,
        "stage": stage,
        "remarks": remarks
    }
    print('prepare_loan_info - ', prepare_loan_info)
    update_perdix_loan = await perdix_update_loan(prepare_loan_info)
    # update_perdix_loan_dict = response_to_dict(update_perdix_loan)
    # update_perdix_loan_dict = json.loads(update_perdix_loan.decode('utf-8'))
    # print('coming after gateway ', update_perdix_loan)


    # loan_update_response = await perdix_update_loan(loan_id)

    # result = get_loan_info
    result = update_perdix_loan

    # print('loan status code ', loan_update_response.status_code)
    # print('loan status content ')
    # print(result)
    # get_perdix_loan_data = await perdix_fetch_loan(loan_id)
    # print('getting customer', get_perdix_data)

    return result

