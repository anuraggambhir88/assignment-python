import requests
from assertpy import assert_that
import pytest
from request_helper import Request,RequestType,Endpoints,StatusCodes,ApiType
from assert_helper import assert_equal,assert_true
from request_model import Debug
import xmlschema
from lxml import etree


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
def test_tc_03_check_xml_api_for_additional_parameter():
    URL = Endpoints.XML + Debug.DEBUG_TRUE + "&additional=true"
    status,response = Request.send_request(RequestType.GET,URL,ApiType.XML,params=None)
    assert_equal(StatusCodes.STATUS_500,status,'statuscode')

# [REQ-3.3] A successful call to the POST /xml endpoint returns a status code of 201
def test_tc_03_check_xml_api_put_returns_201_status_code():
    status,response = Request.send_request(RequestType.PUT,Endpoints.XML,ApiType.XML,params=None)
    assert_that(str(status)).is_equal_to(StatusCodes.STATUS_201) 


# [REQ-3.4] The body of a successful call to the POST /xml endpoint will be of the format:
@pytest.mark.parametrize("debug_value",[(Debug.DEBUG_TRUE),(Debug.DEBUG_FALSE)])
def test_tc_04_check_xsd_schema_against_xml_response(debug_value):
    URL = Endpoints.XML + debug_value
    status,response = Request.send_request(RequestType.GET,URL,ApiType.XML,params=None)
    assert_equal(StatusCodes.STATUS_200,status,'statuscode')
    Request.save_xml_response("xml_response.xml",response)
    if str(debug_value).find("true") >=0:
        assert_true(Request.validate_xml_against_xsd("xml_schema_debug_true.xsd","xml_response.xml"),"Invalid Schema")
    else:
        assert_true(Request.validate_xml_against_xsd("xml_schema_debug_false.xsd","xml_response.xml"),"Invalid_Schema")



# [REQ-3.5] The 'data/decision_engine/overall' item should be 'Accept' unless one of the rules has an outcome of 'Decline' in which case the overall result should be 'Decline'
@pytest.mark.parametrize("debug_value",[(Debug.DEBUG_FALSE),(Debug.DEBUG_TRUE)])
def test_tc_05_check_xml_response_if_any_item_value_is_decline_then_overall_result_will_be_decline(debug_value):
    URL = Endpoints.XML + debug_value
    overall_result_expected = "Accept"
    status,response = Request.send_request(RequestType.GET,URL,ApiType.XML,params=None)
    assert_equal(StatusCodes.STATUS_200,status,'statuscode')
    xml_encoded = etree.fromstring(bytes(response, encoding='utf-8'))
    overall_result_actual = Request.get_xml_data_from_path(xml_encoded,"/data/decision_engine/overall")
    rule_list = Request.get_xml_data_list_from_path(xml_encoded,"//data/decision_engine/outcomes//rule")
    for rule in rule_list(xml_encoded):
        rule_value  = rule.text
        if rule_value == "Decline":
            overall_result_expected= "Decline"

    assert_equal(overall_result_expected,overall_result_actual,"Overall Result")



