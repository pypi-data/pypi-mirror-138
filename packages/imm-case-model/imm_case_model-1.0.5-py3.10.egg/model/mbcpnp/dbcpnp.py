import email
from types import CoroutineType

# Rep model
DRepModel={
    'personal':{
        "last_name":"FAMILYNAMES",
        "first_name":"GIVENNAMES",
        "dob":"DATEOFBIRTHDDMMMYYYY"
    },
    'rcic':{
        "last_name":"REPRESENTATIVESFAMILYNAMES",
        "first_name":"REPRESENTATIVESGIVENNAMES",
        "employer_legal_name":"NAMEOFFIRMORORGANIZATIONIFAPPLICABLE",
        "phone":"PRIMARYPHONENUMBER",
        "alter_phone":"",
        "email":"EMAILADDRESS",
        "street_address":"REPRESENTATIVESMAILINGADDRESSLINE",
        "city":"CITYTOWN", 
        "province":"PROVINCESTATE",
        "country":"COUNTRY",
        "post_code":"POSTALZIPCODE",
        "rcic_number":"MembershipID"
    },
    'employer':{
        "legal_name":"LEGALNAMEOFCOMPANYORGANIZATION",
        "last_name":"EMPLOYERCONTACTFAMILYNAMES",
        "first_name":"EMPLOYERCONTACTGIVENNAMES"
    }
}

# Job offer form model
DJofModel={
    
}

# BCPNP registration model
DRegModel={
    
}

# BCPNP application model
DAppModel={
    
}
