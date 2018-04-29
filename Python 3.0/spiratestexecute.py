import urllib
import urllib.request
import http.client
import time
from xml.sax import saxutils

#       This defines the 'SpiraTestExecute' class that provides the Python facade
#       for calling the SOAP web service exposed by SpiraTest
#       (The current implementation doesn't support SSL connections)
#
#       Author          Inflectra Corporation
#       Version         5.0.0
#       Notes           Requires Python 3.0 or later

class SpiraTestExecute:

        #define the web-service namespace and URL suffix constants
        WEB_SERVICE_NAMESPACE = "http://www.inflectra.com/SpiraTest/Services/v2.2/"
        WEB_SERVICE_URL_SUFFIX = "/Services/v2_2/ImportExport.asmx"

        def recordTestRun(self, testerUserId, testCaseId, releaseId, testSetId, startDate, endDate, executionStatusId, runnerName, runnerTestName, runnerAssertCount, runnerMessage, runnerStackTrace):
                
                #create the SOAP packet body passing through the appropriate parameters
                methodName = 'TestRun_RecordAutomated2'
                optionalParameters = ''
                if releaseId != -1:
                        optionalParameters += '<releaseId>' + str(releaseId) + '</releaseId>\r\n'
                if testSetId != -1:
                        optionalParameters += '<testSetId>' + str(testSetId) + '</testSetId>\r\n'
                body= \
                        '<?xml version="1.0" encoding="utf-8"?>\r\n' + \
                        '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\r\n' + \
                                '<soap:Body>\r\n' + \
                                        '<' + methodName + ' xmlns="' + self.WEB_SERVICE_NAMESPACE + '">\r\n' + \
                                                '<userName>' + saxutils.escape(self.userName) + '</userName>\r\n' + \
                                                '<password>' + saxutils.escape(self.password) + '</password>\r\n' + \
                                                '<projectId>' + str(self.projectId) + '</projectId>\r\n' + \
                                                '<testerUserId>' + str(testerUserId) + '</testerUserId>\r\n' + \
                                                '<testCaseId>' + str(testCaseId) + '</testCaseId>\r\n' + \
                                                optionalParameters + \
                                                '<startDate>' + time.strftime('%Y-%m-%dT%H:%M:%S',startDate) + '</startDate>\r\n' + \
                                                '<endDate>' + time.strftime('%Y-%m-%dT%H:%M:%S',endDate) + '</endDate>\r\n' + \
                                                '<executionStatusId>' + str(executionStatusId) + '</executionStatusId>\r\n' + \
                                                '<runnerName>' + runnerName + '</runnerName>\r\n' + \
                                                '<runnerTestName>' + runnerTestName + '</runnerTestName>\r\n' + \
                                                '<runnerAssertCount>' + str(runnerAssertCount) + '</runnerAssertCount>\r\n' + \
                                                '<runnerMessage>' + saxutils.escape(runnerMessage) + '</runnerMessage>\r\n' + \
                                                '<runnerStackTrace>' + saxutils.escape(runnerStackTrace) + '</runnerStackTrace>\r\n' + \
                                        '</' + methodName + '>\r\n' + \
                                '</soap:Body>\r\n' + \
                        '</soap:Envelope>\r\n'

                #create the SOAP header using the sessionless version of the SpiraTest Record API
                headers = {
                        'Content-Type' : 'text/xml; charset=utf-8',
                        'SOAPAction' : '"' + self.WEB_SERVICE_NAMESPACE + methodName + '"'
                        }
                
                #actually call the SpiraTest API - we can simply ignore the return value
                if self.ssl:
                        connection = http.client.HTTPSConnection(self.server, self.port)
                else:
                        connection = http.client.HTTPConnection(self.server, self.port)
                
                #connection.set_debuglevel(1)
                connection.request("POST", "/" + self.path + self.WEB_SERVICE_URL_SUFFIX, body, headers)
                response = connection.getresponse()
                output = response.read()
                if response.status == 200:
                        print("Successfully recorded the result for test case: " + str(testCaseId))
                else:
                        print ("Failed to send results to SpiraTest: ", response.status, response.reason, output)
