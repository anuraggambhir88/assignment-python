# QA Python Coding Exercise

## The Task

- Get the server up and running
- Write tests covering as many requirements as possible as detailed in the Requirements.md file


##Issue 1: 
-API - /Version did support DELETE 
-Solution : Fixed in the API by disabling the Delete Call
-Removed "@app.get("/version/")"


##Issue 2 : 
-API: /Json 
-Product Version - is Number not float

##Issue 3 : 
-API: /Json
-Response time is coming greater than 200ms randomly 

##Issue 5:
-API /Json
-Input Parameter ProductName in requirement : CREDITCARDS , Accepted Parameter : CREDITCARD


##Issue 6
-API: /XML
-XML was not valid (? was missing in xml declaration) 
-Fixed by adding ? in the xml declaration

##Issue 7
-API: /XML
-Space in the start(issue in parsing)
-Fixed by removing extra space in XML schema creation

##Issue 8 
-API: /XML
-Any inside rule when set to "decline" is not setting the overall result to "decline"
-Fixed by chaging logic of the API added following code in the api implementation
-if rule_outcome == "Decline": //if any rule outcome is decline it will
-    overall_result = "Decline" //change the overall result

##Issue 9 
-API : /XML
-Issue : Success call to POST /XML should return 201 status code 
-No Post call present for /XML endpoint in the API code -Conflicting requirement [3.1 and 3.3] 

##Issue 10
-API : / XML
- [REQ-3.2] The /xml endpoint supports a single query parameter: False supporting additional parameter 
