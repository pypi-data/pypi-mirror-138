from datetime import date
from pydantic import BaseModel
from typing import Optional

class Marriage(BaseModel):
    marital_status:str
    married_date:Optional[date]
    sp_last_name:Optional[str]
    sp_first_name:Optional[str]
    
    previous_married:bool
    pre_sp_last_name:Optional[str]
    pre_sp_first_name:Optional[str]
    pre_relationship_type:Optional[str]
    pre_start_date:Optional[date]
    pre_end_date:Optional[date]
    
class PersonId(BaseModel):
    id_type:str
    type_of_id:str
    number:Optional[str]
    country:Optional[str]
    issue_date:Optional[date]
    expiry_date:Optional[date]

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
    
    native_language:Optional[str]
    english_french:Optional[str]
    which_one_better:Optional[str]
    language_test:Optional[str]
    
    current_country:str
    current_country_status:str
    current_status_start_date:date
    current_status_end_date:Optional[date]
    other_status:Optional[str]
    
# Not everyone has education. So, it's optional. Without start date and end date, the app will regard having no education
class Education(BaseModel):
    start_date:Optional[date]
    end_date:Optional[date]
    school_name:Optional[str]
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
    last_name	
    first_name	
    native_last_name	
    native_first_name	
    marital_status	
    date_of_birth	
    place_of_birth	
    birth_country	
    country_of_citizenship	
    address
    occupation	
    relationship	
    email	
    date_of_death	
    place_of_Death	
    accompany_to_canada