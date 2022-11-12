import requests
import pytest
from request_helper import Request,RequestType,Endpoints,StatusCodes,ApiType
from assert_helper import assert_equal,assert_true
from request_model import VersionData,Entity
import re

# [REQ-1.1] The /version endpoint only supports the GET method.
@pytest.mark.parametrize("method, statuscode",[(RequestType.GET,StatusCodes.STATUS_200),
                                            (RequestType.PUT,StatusCodes.STATUS_405),
                                            (RequestType.POST,StatusCodes.STATUS_405),
                                            (RequestType.DELETE,StatusCodes.STATUS_405)])
def test_tc_01_check_user_version_api_only_support_get_method(method,statuscode):
    status,response = Request.send_request(method,Endpoints.VERSION,ApiType.JSON,params=None)
    assert_equal(statuscode,status,'statuscode')

# [REQ-1.2] The /version endpoint returns a status code of '200 OK' and a response body of the format:
# ```json
#   {
#     "success": true,
#     "data": {
#         "version": <Version>
#     }
#   }
# ```
def test_tc_02_check_user_version_status_code_and_body():
    status,response = Request.send_request(RequestType.GET,Endpoints.VERSION,ApiType.JSON,params=None)
    assert_equal(StatusCodes.STATUS_200,status,'statuscode')
    assert_true(response[Entity.success],"Success entity value is not true")
    pattern = re.compile(VersionData.version_format)
    assert_true(bool(pattern.match(str(response[Entity.data][Entity.version]))),"Version is not in X.X.X format")
    
# [REQ-1.3] Any other HTTP methods executed against the /version endpoint will return a status code of '405 Method Not Allowed' and a response body of the format:
@pytest.mark.parametrize("method, statuscode",[(RequestType.PUT,StatusCodes.STATUS_405),(RequestType.POST,StatusCodes.STATUS_405),(RequestType.DELETE,StatusCodes.STATUS_405)])
def test_tc_03_check_user_version_response_with_other_http_methods(method,statuscode):
    status,response = Request.send_request(method,Endpoints.VERSION,ApiType.JSON,params=None)
    assert_equal(statuscode,status,'statuscode')
    assert_equal(response[Entity.detail],"Method Not Allowed","Detail Attribute ")


