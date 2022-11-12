import requests
import pytest
from request_helper import Request,RequestType,Endpoints,StatusCodes,ApiType
from assert_helper import assert_equal,assert_true
from request_model import JsonApiReqParams,JsonEntity,ProductName
import re

params = {JsonApiReqParams.product_name:JsonApiReqParams.product_name_value,
        JsonApiReqParams.product_type:JsonApiReqParams.product_type_value,
        JsonApiReqParams.product_version:JsonApiReqParams.product_version_value}



# [REQ-1.1] The /version endpoint only supports the GET method.
@pytest.mark.parametrize("method, statuscode",[(RequestType.POST,StatusCodes.STATUS_200),
                                            (RequestType.PUT,StatusCodes.STATUS_405),
                                            (RequestType.GET,StatusCodes.STATUS_405),
                                            (RequestType.DELETE,StatusCodes.STATUS_405)])
def test_tc_01_check_json_api_only_support_post_method(method,statuscode):
    status,response = Request.send_request(method,Endpoints.JSON,ApiType.JSON,params)
    assert_equal(statuscode,status,'statuscode')




# [REQ-2.2] The request body for the /json endpoint is of the format:
# ```json
# {
#     "product_name": "<String>",
#     "product_type": "<String>",
#     "product_version": <Float>
# Where the data must obey the following conditions:

# | Field Name | Data Type | Allowed Values                         |
# |------------|-----------|----------------------------------------|
# | product_name | String | SAVINGS, LOANS, MORTGAGES, CREDITCARDS |
# | product_type | String | Any                                    |
# | product_version | Float | Positive floats (E.g. 1.1, 2.1)        |

@pytest.mark.parametrize("product_name_value",[("SAVINGS"),("LOANS"),("MORTGAGES"),("OTHER"),("CREDITCARD")])
def test_tc_02_check_json_api_product_name_request_value(product_name_value):
    params.update({JsonApiReqParams.product_name:product_name_value})
    status,response = Request.send_request(RequestType.POST,Endpoints.JSON,ApiType.JSON,params)
    product_name_values = set(product.value for product in ProductName)
    if product_name_value in product_name_values:
        assert_equal(StatusCodes.STATUS_200,status,'statuscode')
    else:
        assert_equal(StatusCodes.STATUS_400,status,'statuscode')

@pytest.mark.parametrize("product_type_value",[("account"),(1),(1.0)])
def test_tc_03_check_json_api_product_type_request_value(product_type_value):
    params.update({JsonApiReqParams.product_type:product_type_value})
    response = requests.post(Endpoints.JSON,json=params)
    if isinstance(product_type_value,str):
        assert_equal(StatusCodes.STATUS_200,response.status_code,'statuscode')
    else:
        assert_equal(StatusCodes.STATUS_500,response.status_code,'statuscode')

@pytest.mark.parametrize("product_version_value",[(1.0),(99.0),(1)])
def test_tc_04_check_json_api_product_version_request_value(product_version_value):
    params.update({JsonApiReqParams.product_version:product_version_value})
    response = requests.post(Endpoints.JSON,json=params)
    if isinstance(product_version_value,float):
        assert_equal(StatusCodes.STATUS_200,response.status_code,'statuscode')
    else:
        assert_equal(StatusCodes.STATUS_500,response.status_code,'statuscode')










# [REQ-2.3] The successful response body of the /json endpoint is of the format

# ```json
# {
#     "format": "JSON",
#     "data": {
#         "product_name": "<String>",
#         "product_type": "<String>",
#         "product_version": <Float>,
#     },
#     "additional": {
#         "overall": {
#             "duration": <Float>,
#             "result": "<String>"
#         },
#         "decisions": [
#             {
#                 "rule[Code]": {
#                     "duration": <Float>,
#                     "result": "<String>"
#                 },
#                 ...
#             }
#         ]
#     }
# }
# ```




# [REQ-2.4] All other methods will result in a status code of '405 Method Not Allowed' and a response body of the format:
@pytest.mark.parametrize("method, statuscode",[(RequestType.PUT,StatusCodes.STATUS_405),
                                            (RequestType.GET,StatusCodes.STATUS_405),
                                            (RequestType.DELETE,StatusCodes.STATUS_405)])
def test_tc_04_check_json_api_response_with_other_http_methods(method,statuscode):
    status,response = Request.send_request(method,Endpoints.JSON,ApiType.JSON,params)
    assert_equal(statuscode,status,'statuscode')
    assert_equal(response[JsonEntity.detail],"Method Not Allowed","Detail Attribute ")


# [REQ-2.5] The/response time for the /json call should always be a sub 200ms response time.
def test_tc_05_check_json_api_response_time_is_less_than_200ms():
    response = requests.post(Endpoints.JSON,json=params) 
    assert_true(int(response.elapsed.microseconds/1000) < 200,"Response time is greater than 200ms")