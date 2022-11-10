import json
from fastapi import Header, HTTPException
from fastapi.encoders import jsonable_encoder
from dm_nac_service.resource.logging_config import logger
from dm_nac_service.utils import get_env_or_fail
from dm_nac_service.config.database import get_database

BBPS='bbps'


def get_token_header(x_token: str = Header(...)):
    x_token = get_env_or_fail(BBPS, 'x-token', BBPS + ' x-token not configured')
    if x_token != x_token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


def response_to_dict(response):
    """Converting bytes response to python dictionary"""
    response_content = response.content
    response_decode = response_content.decode("UTF-8")
    json_acceptable_string = response_decode.replace("'", "\"")
    convert_to_json = json.loads(json_acceptable_string)
    response_dict = dict(convert_to_json)
    return response_dict


def response_bytes_to_dict(response):
    """Converting bytes response to python dictionary"""
    response_content = response.content
    response_decode = response_content.decode("utf-8")
    convert_to_json = json.loads(response_decode)
    # response_dict = convert_to_json[0]
    # return response_dict
    return convert_to_json


def hanlde_response_body(body_data):
    try:
        body_data_decode = jsonable_encoder(body_data)
        response_body = body_data_decode.get('body')
        
       
        if 'error' in response_body:
            response_body_json = json.loads(response_body)
            # response_body_error = response_body_json.get('error')
            # response_body_description = response_body_json.get('error_description')
            # response_to_return = {"error": response_body_error, "error_description": response_body_description}
            response_to_return = response_body_json
        else:
            response_body_string = response_body
            response_to_return = json.loads(response_body_string)
        return response_to_return
    except Exception as e:
        logger.exception(f"Exception inside hanlde_response_body from generics {e.args[0]}")


def hanlde_response_status(body_data):
    try:
        body_data_decode = jsonable_encoder(body_data)
       
        response_body_status = body_data_decode.get('status_code')
        return response_body_status
    except Exception as e:
        logger.exception(f"Exception inside hanlde_response_status from generics {e.args[0]}")


async def fetch_data_from_db(table):
    try:
        database = get_database()
        query = table.select()
        record_array = await database.fetch_all(query)
        return record_array
    except Exception as e:
        logger.exception(f"Exception inside fetch_data_from_db from generics {e.args[0]}")