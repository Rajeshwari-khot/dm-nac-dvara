from pydantic import BaseModel
from typing import Optional

class CreateDisbursement(BaseModel):
    originator_id:str
    sanction_reference_id:str
    customerId:str
    requestedAmount:str
    ifscCode:str
    branchName:str
    processingFees:str
    insuranceAmount:str
    DisbursementDate:str
