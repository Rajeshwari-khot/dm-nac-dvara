

from fastapi import APIRouter, Depends, status, File, UploadFile, Form, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database



from gateway.nac_disbursement import nac_disbursement, disbursement_get_status
from data.database import get_database, sqlalchemy_engine, insert_logs

from app_responses.disbursement import disbursement_request_success_response, disbursement_request_error_response1, disbursement_request_error_response2, disbursement_request_error_response3, disbursement_status_success_response1, disbursement_status_success_response2, disbursement_status_error_response1, disbursement_status_error_response2, disbursement_status_error_response3


from data.disbursement_model import (
    disbursement,
    DisbursementBase,
    DisbursementDB,
    CreateDisbursement
)

from data.sanction_model import (
sanction
)

router = APIRouter()





@router.post("/find-customer-sanction", tags=["Sanction"])
async def find_customer_sanction(
        loan_id
):
    try:
        
        database = get_database()
        select_query = sanction.select().where(sanction.c.loan_id == loan_id).order_by(sanction.c.id.desc())
       
        raw_sanction = await database.fetch_one(select_query)
        sanction_dict = {
            "customerId": raw_sanction[1],
            
            "sanctionRefId": raw_sanction[2]
        }
        print( '*********************************** SUCCESSFULLY FETCHED CUSTOMER ID AND SANCTION REFERENCE ID FROM DB  ***********************************')
        
        result = sanction_dict
        if raw_sanction is None:
            return None

        
    except Exception as e:
        print(
            '*********************************** FAILURE FETCHING CUSTOMER ID AND SANCTION REFERENCE ID FROM DB  ***********************************')
        log_id = await insert_logs('MYSQL', 'DB', 'find_customer_sanction', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Issue with fetching dedupe ref id from db, {e.args[0]}"})
    return result


async def get_disbursement_or_404(
    disbursement_reference_id: int
) -> DisbursementDB:
    database = get_database()
   
    select_query = disbursement.select().where(disbursement.c.disbursement_reference_id == disbursement_reference_id)
   
    raw_disbursement = await database.fetch_one(select_query)
    
    if raw_disbursement is None:
        return None

    return DisbursementDB(**raw_disbursement)


@router.post("/disbursement", tags=["Disbursement"])
async def create_disbursement(
    
    disbursement_data
    
):
    try:
        database = get_database()
        

        disbursement_data_dict = disbursement_data
        
        sanction_reference_id = disbursement_data_dict['sanctionReferenceId']

        disbursement_response = await nac_disbursement('disbursement', disbursement_data_dict)
        print('response from disburmsent info', disbursement_response)

        disbursement_response_status = disbursement_response['content']['status']
        disbursement_response_message = disbursement_response['content']['message']
        store_record_time = datetime.now()
        disbursement_info = {
            'customer_id': disbursement_data_dict['customerId'],
            'originator_id': disbursement_data_dict['originatorId'],
            'sanction_reference_id': disbursement_data_dict['sanctionReferenceId'],
            'requested_amount': disbursement_data_dict['requestedAmount'],
            'ifsc_code': disbursement_data_dict['ifscCode'],
            'branch_name': disbursement_data_dict['branchName'],
            'processing_fees': disbursement_data_dict['processingFees'],
            'insurance_amount': disbursement_data_dict['insuranceAmount'],
            'disbursement_date': disbursement_data_dict['disbursementDate'],
            'created_date': store_record_time,
        }
        disbursement_response_status = disbursement_response['content']['status']
        if(disbursement_response_status == 'SUCCESS'):
            disbursement_info['message'] = disbursement_response_message
            disbursement_info['status'] = disbursement_response_status
            disbursement_info['disbursement_reference_id'] = disbursement_response['content']['value']['disbursementReferenceId']
            insert_query = disbursement.insert().values(disbursement_info)
            
            disbursement_id = await database.execute(insert_query)

        else:
            disbursement_info['message'] = disbursement_response_message
            disbursement_info['status'] = disbursement_response_status

        

        result = disbursement_response
        print('SUCCESSFULLY COMING OUT OF CREATE DISBURSEMENT ', result)
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Issue with Northern Arc API, {e.args[0]}"})
    return result


@router.get("/disbursement-status", tags=["Disbursement"])
async def get_disbursement_status(
    disbursement_reference_id, database: Database = Depends(get_database)
):
    try:
        print('coming inside of disbursement status', disbursement_reference_id)
       
        disbursement_status_response = await disbursement_get_status('disbursement', disbursement_reference_id)
        

        result = disbursement_status_response
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Issue with Northern Arc API, {e.args[0]}"})
    return result