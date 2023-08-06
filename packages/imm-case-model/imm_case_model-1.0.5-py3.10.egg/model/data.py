class DataDefinition():
    Male="M"
    Female="F"
    Unknown="U"
    sexes=[
        (Male,"Male"),
        (Female,"Female"),
        (Unknown,'Unknown')
    ]

    MARRIAGE_STATUS=[
        ("Married",'Married'),
        ("Never_Married",'Never married'),
        ("Common_law partner",'Common law partner'),
        ("Separated",'Separated'),
        ("Divorced",'Divorced'),
        ("Widowed",'Widowed')
    ]

    RELATIONSHIP=[
        ("Brother",'Brother'),
        ("Sister",'Sister'),
        ("Father",'Father'),
        ("Mother",'Mother')    # TODO: 需要添加
    ]
    PROVINCE=[
        ("NL","Newfoundland and Labrador"),
        ("PE","Prince Edward Island"),
        ("NS","Nova Scotia"),
        ("NB","New Brunswick"),
        ("QC","Quebec"),
        ("ON","Ontario"),
        ("MB","Manitoba"),
        ("SK","Saskatchewan"),
        ("AB","Alberta"),
        ("BC","British Columbia"),
        ("YT","Yukon"),
        ("NT","Northwest Territories"),
        ("NU","Nunavut")
    ]
    EYE_COLOR=[
        ("Black","Black"),
        ("Brown","Brown"),
        ("Green","Green") # TODO: 
    ]

    EDUCATION_LEVEL = [
        ("Doctor",'Doctor'),
        ("Master",'Master'),
        ("Professional",'Professional'),
        ("Bachelor",'Bachelor'), 
        ("Associate_Degree",'Associate Degree'),
        ("Post_Secondary",'Post Secondary'),
        ("Secondary",'Secondary'),
        ("Other",'Other')
        ]

    LANGUAGE_TEST_TYPE=[
        ("IELTS_General",'IELTS General'),
        ("IELTS_Academic",'IELTS Academic'),
        ("CELPIP_General",'CELPIP General'),
        ("CELPIP_Academic",'CELPIP Academic'),
        ("TEF",'TEF'),
        ("TCF",'TCF')
    ]
    WORK_PERMIT=[
        ('PGWP',"Post Graduate Work Permit"),
        ('OWP',"Open Work Permit"),
        ('WP_LMIA','Work Permit supported by LMIA'),
        ('WP_SP','Work under Study Permit') # TODO: 需要继续归类
    ] 
    PHONE_TYPE=[
        ('Cell','Cell Phone'),
        ('Home','Home Phone'),
        ('Work','Work Phone'),
        ('Fax','Fax Phone')
    ]   
