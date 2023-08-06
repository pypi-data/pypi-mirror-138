from model.pdfformmodel import pdfformmodel
import json

class F1295(pdfformmodel):
    excluded_keys={
        'personal':[],
        'marital_status':[]
    }

    pairs={
        'personal':{
            "name":"school_name",
            "PlaceBirthCity":"level",
            "PlaceBirthCountry":"field_of_study"
        },
        'marital_status':{
            "MaritalStatus":"company",
            "DateOfMarriage":"duties",
            'FamilyName':"job_title"
        }
    }
    paths={
        'personal':['form1','Page1','PersonalDetails'],
        'marital_status':['form1','Page1','MaritalStatus','SectionA']
    }


