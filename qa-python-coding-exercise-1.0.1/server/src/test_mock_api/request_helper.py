import json
import requests
from requests import RequestException
from lxml import etree

from pathlib import Path
import xmlschema

class Request:

    @staticmethod
    def send_request(method, endpoint, type, params=None):
        try:
            print("********************************************")
            print("Request URL" + str(endpoint))
            print("********************************************")

            print("********************************************")
            print("Request Method" + str(method))
            print("********************************************")

            print("********************************************")
            print("Request Params" + str(params))
            print("********************************************")

            if method == RequestType.DELETE:
                response = method(endpoint)
            else:
                response = method(endpoint, json = params)

            print("Response Status code " + str(response.status_code))
            print("Response" + str(response.text))
            print("********************************************")
            if type == "json":
                return response.status_code, json.loads(response.text)
            else:
                return response.status_code, response.text
        except RequestException as e:
            print('Issue in request type {} : expection {}'.format(method,e))

    @staticmethod
    def format_xml(response_text):
        return etree.fromstring(bytes(response_text, encoding='utf8'))

    @staticmethod
    def save_xml_response(file_name,response):
        f_response = Path(__file__).with_name(file_name)
        with open(f_response, 'w') as f:
            f.write(response)
            
    @staticmethod
    def get_xml_data_from_path(xml_encoded,xpath):
        return xml_encoded.xpath(xpath)[0].text

    @staticmethod
    def get_xml_data_list_from_path(xml_encoded,xpath):
        return etree.XPath(xpath)
    

    @staticmethod
    def validate_xml_against_xsd(xsd_file,xml_file):
        xsd_file_path = Path(__file__).with_name(xsd_file)
        xml_file_path = Path(__file__).with_name(xml_file)
        print(xsd_file_path)
        my_schema = xmlschema.XMLSchema(xsd_file_path)
        return my_schema.is_valid(xml_file_path)



class RequestType:
    GET = requests.get
    POST = requests.post
    PUT = requests.put
    DELETE = requests.delete


class StatusCodes:
    STATUS_200 = '200'
    STATUS_405 = '405'
    STATUS_201 = '201'
    STATUS_400 = '400'
    STATUS_500 = '500'

class Base:
    BASE_URL = "http://127.0.0.1:8000"

class Endpoints:
    VERSION = Base.BASE_URL + "/version"
    JSON = Base.BASE_URL + "/json"
    XML = Base.BASE_URL + "/xml/"
    
class ApiType:
    XML = "xml"
    JSON = "json"







    
