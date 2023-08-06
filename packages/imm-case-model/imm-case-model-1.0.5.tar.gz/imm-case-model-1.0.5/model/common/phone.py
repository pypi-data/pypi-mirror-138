from pydantic import BaseModel
from typing import Optional
from collections import namedtuple
from model.common.mixins import EqMixin

class Phone(BaseModel,EqMixin):
    variable_type:str
    display_type:str
    country_code:Optional[int]
    number:Optional[int]
    ext:Optional[int]
    

    class Config:
        anystr_lower=True 
    
    @property
    def international_format_full(self):
        return '+'+str(self.country_code)+" "+str(self.number)
    
    @property
    def isCanadaUs(self):
        return self.country_code and self.country_code==1
    
    @property
    def is_fax(self):
        return self.v_type=='fax'
    
    @property
    def NA_format_number(self):
        if len(str(self.number))!=10:
            raise ValueError(f"{self.number} is not a valid North America phone number")
        return '('+str(self.number)[:3]+') '+str(self.number)[3:6]+'-'+str(self.number)[6:]
    
        
    # Return a list including area code, first part and second part of number
    @property
    def NA_format_list(self):
        if len(str(self.number))!=10:
            raise ValueError(f"{self.number} is not a valid North America phone number")
        return [str(self.number)[:3],str(self.number)[3:6],str(self.number)[6:]]
    
    # Return a list including area code, first part and second part of number
    @property
    def NA_format_namedtuple(self):
        if len(str(self.number))!=10:
            raise ValueError(f"{self.number} is not a valid North America phone number")
        NA_Number=namedtuple('NA_Number',['area_code','part1','part2'])
        number=NA_Number(str(self.number)[:3],str(self.number)[3:6],str(self.number)[6:])
        return number
    
    def __str__(self):
        return self.international_format_full

