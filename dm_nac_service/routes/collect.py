

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from dm_nac_service.schemas.collect import CollectBase
from dm_nac_service.services.collect import collect_services

router = APIRouter()

TRANSACTION_NAMES = ['Advance Repayment', 'Overdue-Payment', 'Pre-payment', 'Scheduled Demand', 'Fee Payment', 'Scheduled-Payment', 'Pre-Closure']

INSTRUMENT_TYPES = ['UPI', 'CASH', 'CASH_PAID_ON_DELIVERY', 'CASHBACK', 'DEBIT_CARD', 'DISPUTE', 'NEFT', 'IMPS', 'NACH', 'NEFT_RTGS', 'NETBANKING', 'REFUND', 'SHIPMENT', 'CHEQUE', 'EARLY_PAY_DISCOUNT']

@router.post("/collect", tags=["Collect"])
async def create_collect(
    request_info : CollectBase , transaction_name: str = Query("Transaction Names", enum=TRANSACTION_NAMES), instrument_types: str = Query("Instrument Types", enum=INSTRUMENT_TYPES)
):
    try:
        collect_data_dict = request_info.dict()
       
        collect_response = await collect_services(collect_data_dict)
        result = collect_response
    except Exception as e:
        result = JSONResponse(status_code=500, content={"message": f"Issue with Northern Arc API, {e.args[0]}"})
    return result