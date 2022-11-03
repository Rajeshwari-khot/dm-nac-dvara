from datetime import datetime
from databases import Database
from fastapi import APIRouter, Depends, UploadFile,  Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import dm_nac_service.services.sanction as sanction_services
from dm_nac_service.resource.logging_config import logger
from dm_nac_service.schemas.sanction import CreateSanction
from dm_nac_service.config.database import get_database

NAC_SERVER = 'northernarc-server'
PERDIX_SERVER = 'perdix-server'

FILE_CHOICES = ['SELFIE', 'AADHAR_XML', 'MITC', 'VOTER_CARD', 'DRIVING_LICENSE', 'SANCTION_LETTER', 'PAN', 'PASSPORT', 'AADHAR_DOC', 'LOAN_APPLICATION', 'LOAN_AGREEMENT']

router = APIRouter()


@router.post("/find-sanction", tags=["Sanction"])
async def find_sanction(
        loan_id
):
    """post method for fetching sanction details"""
    try:
        get_find_sanction = await sanction_services.find_sanction(loan_id)

        result = get_find_sanction
    except Exception as e:
        logger.exception(f"{datetime.now()} - routes - sanction - find_sanction {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})


@router.post("/sanction", tags=["Sanction"])
async def create_sanction(request_info : CreateSanction):
    try:
        payload = request_info.dict()
        create_sanction_response = await sanction_services.sanction_service(payload)
        return create_sanction_response
    except Exception as e:
        logger.exception(f"routes - sanction - create_sanction - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})




@router.post("/fileupload", tags=["Sanction"])
async def fileupload_sanction(
        customer_id: str, file: UploadFile, file_type: str = Query("File Types", enum=FILE_CHOICES),  database: Database = Depends(get_database)
):
    try:
        file_upload_info=await sanction_services.file_upload_service(customer_id, file, file_type)
        return file_upload_info
    except Exception as e:
        logger.exception(f"routes - file upload - fileupload_sanction - {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})





@router.get("/sanction-status", tags=["Sanction"])
async def sanction_status(
        customer_id: str, database: Database = Depends(get_database)
):
    """get method for sanction_status"""
    """sent customer_id to northern_arc sanction_status endpoint"""
    """get response as sanction data for that customer_id  """
    try:
        get_sanction_response = await sanction_services.get_sanction_service(customer_id)
        return get_sanction_response
    except Exception as e:
        logger.exception(f"routes - get-sanction-status - sanction_status , {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})       



@router.get("/download-upload-loan-document",  tags=["Sanction"])
async def download_and_upload_file(customer_id, document_id):
    """get method for download document from download_file_from_stream function"""
    """upload document into northern_arc file_upload endpoint"""
    try:
        download_file_from_stream_response = await sanction_services.download_file_from_stream_service(document_id)
        return download_file_from_stream_response
    except Exception as e:
        logger.exception(f"routes - get-download_and_upload_file - , {e.args[0]}")
        return JSONResponse(status_code=500, content={"message": f"{e.args[0]}"})       

