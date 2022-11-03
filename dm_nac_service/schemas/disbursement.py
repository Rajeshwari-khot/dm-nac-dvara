from typing import Optional

import sqlalchemy
from pydantic import BaseModel



class DisbursementBase(BaseModel):
    originatorId: str
    sanctionReferenceId: int
    customerId:str
    requestedAmount: Optional[float] 
    ifscCode: Optional[str] 
    branchName: Optional[str] 
    processingFees: Optional[float] 
    insuranceAmount: Optional[float] 
    disbursementDate: Optional[str] 


class CreateDisbursement(DisbursementBase):
    pass