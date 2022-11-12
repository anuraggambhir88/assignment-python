import requests
from assertpy import assert_that
from lxml import etree
import pytest
from request_helper import Request,RequestType,Endpoints,StatusCodes,ApiType
from assert_helper import assert_equal,assert_true
from request_model import VersionData,Entity
import json



#[REQ-3.1] The /xml endpoint only supports the GET method.
@pytest.mark.parametrize("method, statuscode",[(RequestType.GET,StatusCodes.STATUS_200),
                                            (RequestType.PUT,StatusCodes.STATUS_405),
                                            (RequestType.POST,StatusCodes.STATUS_405),
                                            (RequestType.DELETE,StatusCodes.STATUS_405)])
def test_tc_01_check_xml_api_only_support_get_method(method,statuscode):
    status,response = Request.send_request(method,Endpoints.XML,ApiType.XML,params=None)
    assert_equal(statuscode,status,'statuscode')


    # xml_tree = etree.fromstring(bytes(response_xml, encoding='utf8'))

# [REQ-3.2] The /xml endpoint supports a single query parameter:

# [REQ-3.3] A successful call to the POST /xml endpoint returns a status code of 201
def test_tc_03_check_xml_api_put_returns_201_status_code():
    status,response = Request.send_request(RequestType.PUT,Endpoints.XML,ApiType.XML,params=None)
    assert_that(str(status)).is_equal_to(StatusCodes.STATUS_201) 


# [REQ-3.4] The body of a successful call to the POST /xml endpoint will be of the format:

# [REQ-3.5] The 'data/decision_engine/overall' item should be 'Accept' unless one of the rules has an outcome of 'Decline' in which case the overall result should be 'Decline'