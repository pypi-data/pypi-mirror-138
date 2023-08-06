from datetime import date
from pydantic import BaseModel,EmailStr,validator
from typing import Optional

# trim additional space 
def trimString(text:str):
    if text:
        return ' '.join(text.split())
    else:
        return ''

# return name with standard format
def normalize(name: str):
    if name:
        return ' '.join(name.split()).title()
    else:
        return ''
    
class Personal(BaseModel):
    last_name:str
    first_name:str
    used_last_name:Optional[str]
    used_first_name:Optional[str]
    sex:str
    dob:date
    uci:Optional[str]
    country_of_birth:str
    place_of_birth:str
    citizen:str
    email:EmailStr
    
    native_language:str
    english_french:str
    which_one_better:Optional[str]
    language_test:bool
    
    _normalize_first_name=validator('first_name',allow_reuse=True,check_fields=False)(normalize)
    _normalize_last_name=validator('last_name',allow_reuse=True,check_fields=False)(normalize)
    _normalize_used_first_name=validator('used_first_name',allow_reuse=True,check_fields=False)(normalize)
    _normalize_used_last_name=validator('used_last_name',allow_reuse=True,check_fields=False)(normalize)
    _normalize_spouse_first_name=validator('spouse_first_name',allow_reuse=True,check_fields=False)(normalize)
    _normalize_spouse_last_name=validator('spouse_last_name',allow_reuse=True,check_fields=False)(normalize)
    
    #TODO:  检查是否有config的方法 让所有str的做trimString
    #TODO: 是否需要考虑tr personal和pr personal 用personal做基类。
    
class Marriage(BaseModel):
    marital_status:str
    married_date:Optional[date]
    sp_last_name:Optional[str]
    sp_first_name:Optional[str]
    previous_married:bool
    pre_sp_last_name:Optional[str]
    pre_sp_first_name:Optional[str]
    pre_relationship_type:Optional[str]
    pre_sp_dob:Optional[date]
    pre_start_date:Optional[date]
    pre_end_date:Optional[date]
    
class PersonId(BaseModel):
    variable_type:str
    display_type:str
    number:Optional[str]
    country:Optional[str]
    issue_date:Optional[date]
    expiry_date:Optional[date]

# Not everyone has education. So, it's optional. Without start date and end date, the app will regard having no education
class Education(BaseModel):
    start_date:Optional[date]
    end_date:Optional[date]
    school_name:Optional[str]
    education_level:Optional[str]
    field_of_study:Optional[str]
    city:Optional[str]
    province:Optional[str]
    country:Optional[str]
    
# Not everyone has employment experience. So, it's optional. Without start date and end date, the app will regard having no post secondary education   
class Employment(BaseModel):
    start_date:Optional[date]
    end_date:Optional[date]
    job_title:Optional[str]
    company:Optional[str]
    city:Optional[str]
    province:Optional[str]
    country:Optional[str]
    
class Travel(BaseModel):
    start_date:Optional[date]
    end_date:Optional[date]
    length:Optional[int]
    destination:Optional[str]
    purpose:Optional[str]
    
class Family(BaseModel):
    last_name:str	
    first_name:str	
    native_last_name:str	
    native_first_name:str
    marital_status:str	
    date_of_birth:Optional[date]	
    # place_of_birth:str	
    birth_country:str	
    # country_of_citizenship:str
    address:str
    occupation:str	
    relationship:str	
    # email:Optional[EmailStr]	
    # date_of_death:Optional[date]	
    # place_of_death:Optional[str]	
    accompany_to_canada:bool

# Countries of Residence    
class COR(BaseModel):
    start_date:date
    end_date:Optional[date]
    country:str
    status:str
    