import urllib
import urllib2
import httplib
import time
from xml.sax import saxutils

#	This defines the 'SpiraTestExecute' class that provides the Python facade
#	for calling the SOAP web service exposed by SpiraTest
#	(The current implementation doesn't support SSL connections)
#
#	Author		Inflectra Corporation
#	Version		1.5.1

class SpiraTestExecute:

	#define the web-service namespace and URL suffix constants
	WEB_SERVICE_NAMESPACE = "http://www.inflectra.com/SpiraTest/Services/v1.2.0/"
	WEB_SERVICE_URL_SUFFIX = "/Services/TestExecute.asmx"

	def recordTestRun(self, testerUserId, testCaseId, releaseId, startDate, endDate, executionStatusId, runnerName, runnerTestName, runnerAssertCount, runnerMessage, runnerStackTrace):
		
		#create the SOAP packet body passing through the appropriate parameters
		body= \
			'<?xml version="1.0" encoding="utf-8"?>\r\n' + \
			'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\r\n' + \
				'<soap:Body>\r\n' + \
					'<RecordTestRun2 xmlns="' + self.WEB_SERVICE_NAMESPACE + '">\r\n' + \
						'<userName>' + saxutils.escape(self.userName) + '</userName>\r\n' + \
						'<password>' + saxutils.escape(self.password) + '</password>\r\n' + \
						'<projectId>' + str(self.projectId) + '</projectId>\r\n' + \
						'<testerUserId>' + str(testerUserId) + '</testerUserId>\r\n' + \
						'<testCaseId>' + str(testCaseId) + '</testCaseId>\r\n' + \
						'<releaseId>' + str(releaseId) + '</releaseId>\r\n' + \
						'<startDate>' + time.strftime('%Y-%m-%dT%H:%M:%S',startDate) + '</startDate>\r\n' + \
						'<endDate>' + time.strftime('%Y-%m-%dT%H:%M:%S',endDate) + '</endDate>\r\n' + \
						'<executionStatusId>' + str(executionStatusId) + '</executionStatusId>\r\n' + \
						'<runnerName>' + runnerName + '</runnerName>\r\n' + \
 						'<runnerTestName>' + runnerTestName + '</runnerTestName>\r\n' + \
 						'<runnerAssertCount>' + str(runnerAssertCount) + '</runnerAssertCount>\r\n' + \
						'<runnerMessage>' + saxutils.escape(runnerMessage) + '</runnerMessage>\r\n' + \
						'<runnerStackTrace>' + saxutils.escape(runnerStackTrace) + '</runnerStackTrace>\r\n' + \
 					'</RecordTestRun2>\r\n' + \
				'</soap:Body>\r\n' + \
			'</soap:Envelope>\r\n'

		#create the SOAP header using the sessionless version of the SpiraTest Record API
		headers = {
			'Content-Type' : 'text/xml; charset=utf-8',
			'SOAPAction' : '"' + self.WEB_SERVICE_NAMESPACE + 'RecordTestRun2"'
			}
		
		#actually call the SpiraTest API - we can simply ignore the return value
		connection = httplib.HTTPConnection(self.server, self.port)
		#connection.set_debuglevel(1)
		connection.request("POST", "/" + self.path + self.WEB_SERVICE_URL_SUFFIX, body, headers)
		response = connection.getresponse()
		output = response.read()
		if response.status == 200:
			print "Successfully recorded the result for test case: " + str(testCaseId)
		else:
			print response.status, response.reason, output
