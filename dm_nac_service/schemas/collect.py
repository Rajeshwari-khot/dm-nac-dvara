from typing import Optional
from pydantic import BaseModel



class CollectBase(BaseModel):
    demandAmount: Optional[int] = 1000
    demandDate: Optional[str] = "2021-11-05"
    partnerLoandId: Optional[str] = "2048290"
    reference: Optional[str] =  "UTRNUMBER"
    repaymentAmount: Optional[int] = 1000
    repaymentDate: Optional[str] = "2021-11-05"
    settlementDate: Optional[str] = "2021-11-05"
    tdsAmount: Optional[int] = 100
    outstandingAmount: Optional[int] = 100