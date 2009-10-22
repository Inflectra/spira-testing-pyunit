import unittest
import spiratestexecute
import time

#	This defines the 'SpiraTestExtension' class used to get the results
#	for a PyUnit test run and export them back to SpiraTest
#
#	Author		Inflectra Corporation
#	Version		2.3.0

class SpiraTestExtension:

	def recordResults(self, testClass, testResult, releaseId=-1, runnerName="PyUnit", testSetId=-1):
		print "Extracting test results for SpiraTest import..."

		#we can't report back the testing time for these test cases so we'll just return back the current date/time
		startDate = time.localtime()
		endDate = time.localtime()
		
		#get the list of tests (passed, failed and errors from the test loader object)
		testMethodNames = unittest.TestLoader().getTestCaseNames(testClass)
		
		#iterate through the list of names and see if they passed, failed or had errors
		for testMethodName in testMethodNames:
			testMethodNameString = str(testMethodName)
			#default to passed
			executionStatus = 2
			stackTrace = ""
			message = "Test Passed"

			#The assert count is 1 for failures and 0 for passes
			assertCount = 0
			
			#see if we can find the test case name in the failures collection
			for failure in testResult.failures:
				failedLongMethodName = str(failure[0])
				#get just the method name itself
				failedMethodName = str(failedLongMethodName.split(" ")[0])

				#if we have a match, change status to failure
				if testMethodNameString == failedMethodName:
					executionStatus = 1
					stackTrace = failure[1]
					message = str(failure[0].failureException)
					assertCount = 1

			#see if we can find the test case name in the errors collection
			for failure in testResult.errors:
				failedLongMethodName = str(failure[0])
				#get just the method name itself
				failedMethodName = str(failedLongMethodName.split(" ")[0])

				#if we have a match, change status to failure
				if testMethodNameString == failedMethodName:
					executionStatus = 1
					stackTrace = failure[1]
					message = str(failure[0].failureException)
					assertCount = 1
			
			#extract the test case id from the name (separated by two underscores)
			testCaseId = int(testMethodNameString.split("__")[1])
			
			#report back what we have found
			print testMethodNameString + " has execution status: " + str(executionStatus)
			spiraTestExecute = spiratestexecute.SpiraTestExecute()
			spiraTestExecute.server = self.server
			spiraTestExecute.port = self.port
			spiraTestExecute.path = self.path
			spiraTestExecute.userName = self.userName
			spiraTestExecute.password = self.password
			spiraTestExecute.projectId = self.projectId
			spiraTestExecute.recordTestRun(-1, testCaseId, releaseId, testSetId, startDate, endDate, executionStatus, runnerName, testMethodNameString, assertCount, message, stackTrace)
