from datetime import datetime

from typing import Optional, List,Union
from pydantic import BaseModel, Field



class DedupeTypes(BaseModel):
    type: Optional[str]
    value: Optional[str]


class DedupePan(BaseModel):
    type: Optional[str]
    value: Optional[str] 


class DedupeAadhar(BaseModel):
    type: Optional[str] 
    value: Optional[str] 

class DedupeTableBase(BaseModel):
    accountNumber: Optional[str]
    contactNumber: Optional[str] 
    customerName: Optional[str] 
    dateOfBirth: Optional[str] 
    loanId: str
    pincode: Optional[str] 
    created_date: datetime = Field(default_factory=datetime.now)


class CreateDedupe(BaseModel):
    accountNumber: Optional[str] 
    contactNumber:Optional[str] 
    customerName: Optional[str] 
    dateOfBirth:Optional[str] 
    kycDetailsList:List[Union[DedupePan,DedupeAadhar]]
    loanId:str
    pincode: Optional[str] 


class DedupeCreate(BaseModel):
   __root__:List[CreateDedupe]
    #   pass


class DedupeDB(DedupeTableBase):
    id: int


class DedupeResponse(DedupeTableBase):
    
    response_type:Optional[str]
    id_type1:Optional[str]
    id_value1:Optional[str]
    id_type2:Optional[str]
    id_value2:Optional[str]
    dedupeReferenceId: Optional[str]
    isDedupePresent: Optional[str]
    

class DedupeResponseDB(DedupeTableBase):
    response_type:Optional[str]
    id_type1:Optional[str]
    id_value1:Optional[str]
    id_type2:Optional[str]
    id_value2:Optional[str]
    dedupeReferenceId: Optional[str]
    isDedupePresent: Optional[str]