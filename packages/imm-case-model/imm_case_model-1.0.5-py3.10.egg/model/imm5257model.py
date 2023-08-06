from termcolor import colored
from functools import reduce
from typing import List,Optional
from model.address import Address
from model.phone import Phone
from model.person import PersonId,Personal,Marriage,Education,Employment
from model.tr import TrCase,TrBackground
from model.commonmodel import CommonModel

class Imm5257Model(CommonModel):
    personal:Personal
    marriage:Marriage
    personid:List[PersonId]
    address:List[Address]
    education:List[Education]
    employment:List[Employment]
    phone:List[Phone]
    trcase:TrCase
    trbackground:TrBackground
    
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self,excels=None,output_excel_file=None):
        # IMM5257 (visa application) will use pa.xlsx and tr.xlsx
        if output_excel_file:
            excels=[
                'template/tr.xlsx',
                'template/pa.xlsx'
            ]
        else:
            if excels is None and len(excels)==0:
                raise ValueError('You must input excel file list as source data for validation')
        super().__init__(excels,output_excel_file,globals())

