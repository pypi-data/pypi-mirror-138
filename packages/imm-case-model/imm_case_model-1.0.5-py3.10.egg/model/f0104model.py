from model.pdfformmodel import pdfformmodel
import json
from model.m0104.f0104_data import data

class F0104(pdfformmodel):
    xml_template='/Users/jacky/learn/try1/f0104e.xml'
    excluded_keys={
        'edu':['BtnSub'],
        'emp':['BtnSub'],
        'travel':['BtnSub']
    }

    pairs={
        'edu':{
            "name":"school_name",
            "position":"level",
            "description":"field_of_study"
        },
        'emp':{
            "name":"company",
            "description":"duties",
            'position':"job_title"
        },
        'travel':{
            "name":"purpose",
            "description":"destination"
        }
    }
    paths={
        'edu':['IMM_0104','Page1','EducationSub','EducationTbl','Row1'],
        'emp':['IMM_0104','Page1','EmploymentSub','EmploymentTbl','Row1'],
        'travel':['IMM_0104','Page1','TravelSub','TravelTbl','Row1']
    }


