
from pydantic import BaseModel
from typing import Optional,List

class Address(BaseModel):
    variable_type:str    # this is the identifier variable 
    display_type: str # actually it is the prompt information
    po_box:Optional[str]
    unit:Optional[str]
    street_number:Optional[str]
    street_name:str
    district:Optional[str]
    city:str
    province:str
    country:str
    post_code:str
    
    @property
    def full_address(self):
        fa=self.po_box+' ' if self.po_box else ''
        fa+=self.unit+' ' if self.unit else ''
        fa+=self.street_no+" " if self.street_no else ""
        fa+=self.street_name
        fa+=", "+self.district+', ' if self.district else ""
        fa+=self.city+', '+self.province+', '+self.country+' '+self.post_code
        return fa
    
    @property
    def line1(self):
        l1=self.po_box+' ' if self.po_box else ''
        l1+=self.unit+' ' if self.unit else ''
        l1+=self.street_no+" " if self.street_no else ""
        l1+=self.street_name
        l1+=", "+self.district+', ' if self.district else ""
        return l1

    @property
    def line2(self):
        l2=self.city+', '+self.province+', '+self.country+' '+self.post_code
        return l2
    
    def __eq__(self,another):
        for k,v in self.__dict__.items():
            if k not in ['v_type','display_type'] and v != getattr(another,k,None):
                return False
        return True
        
    def __str__(self):
        return self.full_address


class Addresses(object):
    def __init__(self, address_list: List[Address]) -> None:
        self.addresses=address_list
    
    def _specific_address(self,v_type):
        address=[address for address in self.addresses if address.v_type==v_type]
        return address[0] if address else None
    
    @property
    def mailing_address(self):
        return self._specific_address('mailing_address')
    
    @property
    def residential_address(self):
        return self._specific_address('residential_address')
    
    @property
    def business_address(self):
        return self._specific_address('business_address')
    
    @property
    def working_address(self):
        return self._specific_address('working_address')
    
    

