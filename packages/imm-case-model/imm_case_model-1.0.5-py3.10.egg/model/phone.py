from pydantic import BaseModel
from typing import Optional
from collections import namedtuple
from model.mixins import EqMixin

class Phone(BaseModel,EqMixin):
    phone_type:str
    type_of_phone:str
    country_code:int
    area_code:int
    number:int
    ext:Optional[int]
    

    class Config:
        anystr_lower=True 
    
    @property
    def international_format_number(self):
        # fn='+'+str(self.country_code)+' '
        number=''
        if self.country_code!=86 or self.phone_type!='cellular':    # China mobile phone doesn't include area code
            number=str(self.area_code)+" " 
        number+=str(self.number)
        if self.phone_type!='cellular':  # all mobile phone doesn't have ext number
            number+=' ext '+str(self.ext) if self.ext else "" 
        return number 
       
    @property
    def international_format_full(self):
        return '+'+str(self.country_code)+" "+self.international_format_number
    
    @property
    def isCanadaUs(self):
        return self.country_code and self.country_code==1
    
    @property
    def is_fax(self):
        return self.phone_type=='fax'
    
    @property
    def NA_format_number(self):
        if len(str(self.number))!=7 or len(str(self.area_code))!=3:
            raise ValueError(f"{self.area_code} {self.number} is not a valid North America phone number")
        return '('+str(self.area_code)+') '+str(self.number)[:3]+'-'+str(self.number)[3:]
    
        
    # Return a list including area code, first part and second part of number
    @property
    def NA_format_list(self):
        if len(str(self.number))!=7 or len(str(self.area_code))!=3:
            raise ValueError(f"{self.area_code} {self.number} is not a valid North America phone number")
        return [str(self.area_code),str(self.number)[:3],str(self.number)[3:]]
    
    # Return a list including area code, first part and second part of number
    @property
    def NA_format_namedtuple(self):
        if len(str(self.number))!=7 or len(str(self.area_code))!=3:
            raise ValueError(f"{self.area_code} {self.number} is not a valid North America phone number")
        NA_Number=namedtuple('NA_Number',['area_code','part1','part2'])
        number=NA_Number(str(self.area_code),str(self.number)[:3],str(self.number)[3:])
        return number
    
    def __str__(self):
        return self.international_format_full

