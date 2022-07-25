
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime



from data.database import get_database, sqlalchemy_engine, insert_logs

from gateway.nac_dedupe import nac_dedupe
from app_responses.dedupe import dedupe_response_data
from data.dedupe_model import (
    DedupeDB,
    DedupeCreate,
    dedupe

)



router = APIRouter()

@router.post("/dedupe", response_model=DedupeDB, tags=["Dedupe"])
async def find_dedupe(
        loan_id
) -> DedupeDB:
    try:
        
        database = get_database()
        select_query = dedupe.select().where(dedupe.c.loan_id == loan_id).order_by(dedupe.c.id.desc())
        
        raw_dedupe = await database.fetch_one(select_query)
        dedupe_dict = {
            "dedupeRefId": raw_dedupe[1],
            "isDedupePresent": raw_dedupe[12],
            "isEligible": raw_dedupe[18],

           
            "message": raw_dedupe[19]
        }
        print( '*********************************** SUCCESSFULLY FETCHED DEDUPE REFERENCE ID FROM DB  ***********************************')
       
        result = dedupe_dict
        if raw_dedupe is None:
            return None

       
    except Exception as e:
        print(
            '*********************************** FAILURE FETCHING DEDUPE REFERENCE ID FROM DB  ***********************************')
        log_id = await insert_logs('MYSQL', 'DB', 'find_dedupe', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Issue with fetching dedupe ref id from db, {e.args[0]}"})
    return result


@router.post("/dedupe", response_model=DedupeDB, tags=["Dedupe"])
async def create_dedupe(
    # Below is to test this function manually
    # Data from model
    # dedupe_data: DedupeCreate,

    #  Data from automator
    automator_data,
    

) -> DedupeDB:
    try:
        database = get_database()

        print('2 - send data to gateway function  - ', automator_data)
        dedupe_response = await nac_dedupe('dedupe', automator_data)
        print('7 - Getting the dedupe reference from nac_dedupe function - ', dedupe_response)
        dedupe_response_decode = jsonable_encoder(dedupe_response)
       
        print('7a - Getting the dedupe reference from nac_dedupe function - ', dedupe_response_decode.get('status_code'))
        dedupe_response_decode_status = dedupe_response_decode.get('status_code')

        
        if(dedupe_response_decode_status == 200):
            print('7b - successfully generated dedupe ref id', )
            # Real API response after passing the dedupe data
            # dedupe_response = await nac_dedupe('dedupe', dedupe_data)

            # Fake Response after passing the result data
            # dedupe_response = dedupe_response_data

            # print('dedupe response from create_dedupe', dedupe_response[0])
            store_record_time = datetime.now()

            # For Real API
            dedupe_response_id = str(dedupe_response['dedupeReferenceId'])

            # For Fake Resopnse
            # dedupe_response_id = str(dedupe_response[0]['dedupeReferenceId'])

           
            # For Real API
            kycdetails_array = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')

            # For Fake Response
            # kycdetails_array = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')

            print('8 - Verify kycdetails_array', len(kycdetails_array))
            if (len(kycdetails_array) == 1):
                # For Real API
                print('9 - preparing  kycdetails_array to store in DB - ', dedupe_response)
                id_type1 = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')[0].get('type')
                id_value1 = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')[0].get('value')
                id_type2 = ""
                id_value2 = ""

                # For Fake Response
                # id_type1 = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')[0].get('type')
                # id_value1 = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')[0].get('value')
                # id_type2 = ""
                # id_value2 = ""
            else:

                # For Real API

                id_type1 = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')[0].get('type')
                id_value1 = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')[0].get('value')
                id_type2 = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')[1].get('type')
                id_value2 = dedupe_response.get('dedupeRequestSource').get('kycDetailsList')[1].get('value')
                print('9 - preparing  kycdetails_array to store in DB - ', dedupe_response)

                # For Fake Response
                # id_type1 = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')[0].get('type')
                # id_value1 = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')[0].get('value')
                # id_type2 = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')[1].get('type')
                # id_value2 = dedupe_response[0].get('dedupeRequestSource').get('kycDetailsList')[1].get('value')

            # For Real API
            loan_id = dedupe_response['dedupeRequestSource']['loanId']
            print('printing dedupe result set', dedupe_response['results'])
            dedupe_response_result = len(dedupe_response['results'])
            print('dedupe_response_result - ', dedupe_response_result)
            if (dedupe_response_result > 0):
                dedupue_info = {
                    'dedupe_reference_id': dedupe_response_id,
                    'account_number': dedupe_response['dedupeRequestSource']['accountNumber'],
                    'contact_number': dedupe_response['dedupeRequestSource']['contactNumber'],
                    'customer_name': dedupe_response['dedupeRequestSource']['customerName'],
                    # 'dob': dedupe_response['dedupeRequestSource']['dateOfBirth'],
                    'loan_id': loan_id,
                    'pincode': dedupe_response['dedupeRequestSource']['pincode'],
                    'response_type': dedupe_response['type'],
                    'dedupe_present': str(dedupe_response['isDedupePresent']),
                    'result_attribute': dedupe_response['results'][0]['attribute'],
                    'result_value': dedupe_response.get('results')[0].get('value', 'NA'),
                    'result_value': dedupe_response['results'][0]['value'],
                    'result_rule_name': dedupe_response['results'][0]['ruleName'],
                    'result_ref_loan_id': dedupe_response['results'][0]['id'],
                    'result_is_eligible': dedupe_response['results'][0]['isEligible'],
                    'result_message': dedupe_response['results'][0]['message'],
                    'ref_originator_id': dedupe_response['referenceLoan']['originatorId'],
                    'ref_sector_id': dedupe_response['referenceLoan']['sectorId'],
                    'ref_max_dpd': dedupe_response['referenceLoan']['maxDpd'],
                    'ref_first_name': dedupe_response['referenceLoan']['firstName'],
                    'ref_date_of_birth': dedupe_response['referenceLoan']['dateOfBirth'],
                    'ref_mobile_phone': dedupe_response['referenceLoan']['mobilePhone'],
                    'ref_account_number_loan_ref': dedupe_response['referenceLoan']['accountNumber'],
                    'id_type1': id_type1,
                    'id_value1': id_value1,
                    'id_type2': id_type2,
                    'id_value2': id_value2,
                    'created_date': store_record_time,
                }
            else:
                dedupue_info = {
                    'dedupe_reference_id': dedupe_response_id,
                    'account_number': dedupe_response['dedupeRequestSource']['accountNumber'],
                    'contact_number': dedupe_response['dedupeRequestSource']['contactNumber'],
                    'customer_name': dedupe_response['dedupeRequestSource']['customerName'],
                    # 'dob': dedupe_response['dedupeRequestSource']['dateOfBirth'],
                    'loan_id': loan_id,
                    'pincode': dedupe_response['dedupeRequestSource']['pincode'],
                    'response_type': dedupe_response['type'],
                    'dedupe_present': str(dedupe_response['isDedupePresent']),
                    # 'result_attribute': dedupe_response['results'][0]['attribute'],
                    # 'result_value': dedupe_response.get('results')[0].get('value', 'NA'),
                    # 'result_value': dedupe_response['results'][0]['value'],
                    # 'result_rule_name': dedupe_response['results'][0]['ruleName'],
                    # 'result_ref_loan_id': dedupe_response['results'][0]['id'],
                    # 'result_is_eligible': dedupe_response['results'][0]['isEligible'],
                    # 'result_message': dedupe_response['results'][0]['message'],
                    # 'ref_originator_id': dedupe_response['referenceLoan']['originatorId'],
                    # 'ref_sector_id': dedupe_response['referenceLoan']['sectorId'],
                    # 'ref_max_dpd': dedupe_response['referenceLoan']['maxDpd'],
                    # 'ref_first_name': dedupe_response['referenceLoan']['firstName'],
                    # 'ref_date_of_birth': dedupe_response['referenceLoan']['dateOfBirth'],
                    # 'ref_mobile_phone': dedupe_response['referenceLoan']['mobilePhone'],
                    # 'ref_account_number_loan_ref': dedupe_response['referenceLoan']['accountNumber'],
                    'id_type1': id_type1,
                    'id_value1': id_value1,
                    'id_type2': id_type2,
                    'id_value2': id_value2,
                    'created_date': store_record_time,
                }

            print('10 - preparing Dedupe data to store in DB - ', dedupue_info)
           

            # For Fake Response
            # dedupue_info = {
            #     'dedupe_reference_id': dedupe_response_id,
            #     'account_number': dedupe_response[0]['dedupeRequestSource']['accountNumber'],
            #     'contact_number': dedupe_response[0]['dedupeRequestSource']['contactNumber'],
            #     'customer_name': dedupe_response[0]['dedupeRequestSource']['customerName'],
            #     'dob': dedupe_response[0]['dedupeRequestSource']['dateOfBirth'],
            #     'loan_id': dedupe_response[0]['dedupeRequestSource']['loanId'],
            #     'pincode': dedupe_response[0]['dedupeRequestSource']['pincode'],
            #     'response_type': dedupe_response[0]['type'],
            #     'dedupe_present': str(dedupe_response[0]['isDedupePresent']),
            #     'result_attribute': dedupe_response[0]['results'][0]['attribute'],
            #     'result_value': dedupe_response[0]['results'][0]['value'],
            #     'result_rule_name': dedupe_response[0]['results'][0]['ruleName'],
            #     'result_ref_loan_id': dedupe_response[0]['results'][0]['id'],
            #     'result_is_eligible': dedupe_response[0]['results'][0]['isEligible'],
            #     'result_message': dedupe_response[0]['results'][0]['message'],
            #     'ref_originator_id': dedupe_response[0]['referenceLoan']['originatorId'],
            #     'ref_sector_id': dedupe_response[0]['referenceLoan']['sectorId'],
            #     'ref_max_dpd': dedupe_response[0]['referenceLoan']['maxDpd'],
            #     'ref_first_name': dedupe_response[0]['referenceLoan']['firstName'],
            #     'ref_date_of_birth': dedupe_response[0]['referenceLoan']['dateOfBirth'],
            #     'ref_mobile_phone': dedupe_response[0]['referenceLoan']['mobilePhone'],
            #     'ref_account_number_loan_ref': dedupe_response[0]['referenceLoan']['accountNumber'],
            #     'id_type1': id_type1,
            #     'id_value1': id_value1,
            #     'id_type2': id_type2,
            #     'id_value2': id_value2,
            #     'created_date': store_record_time,
            # }

            insert_query = dedupe.insert().values(dedupue_info)
            print('query', insert_query)
            dedupe_id = await database.execute(insert_query)
            print('11 - Response of the data after storing in DB - ', dedupe_id)
           
            result = JSONResponse(status_code=200, content=dedupe_response)

            # Fake API response from pdf file
            # dedupe_response = dedupe_response_data
            # print('Fake API response from pdf file ', dedupe_response)
            # store_record_time = datetime.now()
            # dedupue_info = {
            #     'dedupe_reference_id': dedupe_response[0]['dedupeReferenceId'],
            #     'originator_id': dedupe_response[0]['referenceLoan']['originatorId'],
            #     'account_number': dedupe_get_root[0]['accountNumber'],
            #     'contact_number': dedupe_get_root[0]['contactNumber'],
            #     'customer_name': dedupe_get_root[0]['customerName'],
            #     'dob': dedupe_get_root[0]['dateofBirth'],
            #     'id_type': dedupe_get_root[0]['kycDetailsList'][0]['type'],
            #     'id_value': dedupe_get_root[0]['kycDetailsList'][0]['value'],
            #     'loan_id': dedupe_get_root[0]['loanId'],
            #     'pincode': dedupe_get_root[0]['pincode'],
            #     'created_date': store_record_time,
            # }
            #
        else:
            print('7b - failure generated dedupe ref id', )

            log_id = await insert_logs('MYSQL', 'DB', 'create_dedupe', '500', str(dedupe_response_decode),
                                       datetime.now())
            result = dedupe_response_decode
            print('error from create dedupe', result)

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'create_dedupe', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Issue with Northern Arc API, {e.args[0]}"})
    return result