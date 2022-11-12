from enum import Enum

class VersionData:
    success = True
    version_format = '^(\d+\.)?(\d+\.)?(\*|\d+)$'


class Entity:
    success = 'success'
    version = 'version'
    data = 'data'
    detail = 'detail'   



class JsonApiReqParams:
    product_name = "product_name"
    product_type = "product_type"
    product_version = "product_version"
    product_name_value = "SAVINGS"
    product_type_value = "New"
    product_version_value = 1.0

class ProductName(Enum):
    SAVING = "SAVINGS"
    LOANS = "LOANS" 
    MORTGAGES= "MORTGAGES"
    CREDITCARDS = "CREDITCARD"

class JsonEntity:
    detail = 'detail' 





