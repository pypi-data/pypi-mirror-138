from datetime import date
from pydantic import BaseModel
from typing import Optional,List
from model.address import Address

class TrCase(BaseModel):
    applying_country:str
    applying_stauts:str
    applying_start_date:date
    applying_end_date:Optional[date]
    consent_of_info_release:bool

class TrBackground(BaseModel):
    q1a:bool
    q1b:bool
    q1c:Optional[str]
    q2a:bool
    q2b:bool
    q2c:bool
    q2d:Optional[str]
    q3a:bool
    q3b:Optional[str]
    q4a:bool
    q4b:Optional[str]
    q5:bool
    q6:bool  
    

  
    

    
