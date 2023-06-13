"""Integration tests for the Zowe Python SDK z/OS Jobs package."""
import unittest
import json
import os
from zowe.zos_jobs_for_zowe_sdk import Jobs
from zowe.core_for_zowe_sdk import ProfileManager

FIXTURES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'fixtures')
JOBS_FIXTURES_JSON_JSON_PATH = os.path.join(FIXTURES_PATH, 'jobs.json')
SAMPLE_JCL_FIXTURE_PATH = os.path.join(FIXTURES_PATH, 'sample.jcl')


class TestJobsIntegration(unittest.TestCase):
    """Jobs class integration tests."""

    def setUp(self):
        """Setup fixtures for Jobs class."""
        test_profile = ProfileManager().load(profile_type="zosmf")
        with open(JOBS_FIXTURES_JSON_JSON_PATH, 'r') as fixtures_json:
            self.jobs_fixtures_json = json.load(fixtures_json)
        self.jobs = Jobs(test_profile)

    def test_get_job_status_should_return_the_status_of_a_job(self):
        """Executing the get_job_status method should return the status of a given job"""
        execution_output = self.jobs.submit_from_mainframe(self.jobs_fixtures_json['TEST_JCL_MEMBER'])
        jobname = execution_output['jobname']
        jobid = execution_output['jobid']
        command_output = self.jobs.get_job_status(jobname, jobid)
        self.assertIsNotNone(command_output['status'])

    def test_list_jobs_should_return_valid_spool_information(self):
        """Executing the list_jobs method should return a list of found jobs in JES spool."""
        command_output = self.jobs.list_jobs(owner=self.jobs_fixtures_json['TEST_JCL_OWNER'])
        self.assertIsInstance(command_output, list)
    
    def test_change_job_class(self):
        """Execute the change_jobs_class should execute successfully."""
        execution_output = self.jobs.submit_from_mainframe(self.jobs_fixtures_json['TEST_JCL_MEMBER'])
        jobname = execution_output['jobname']
        jobid = execution_output['jobid']
        command_output = self.jobs.change_jobs_class(jobname, jobid, "A")
        expected_class = self.jobs.get_job_status(jobname, jobid)
        self.assertEqual(expected_class['class'], "A")

    def test_submit_from_mainframe_should_execute_properly(self):
        """Executing the submit_from_mainframe method should execute successfully."""
        command_output = self.jobs.submit_from_mainframe(self.jobs_fixtures_json['TEST_JCL_MEMBER'])
        jobid = command_output['jobid']
        self.assertIsNotNone(jobid)

    def test_submit_from_local_file_should_execute_properly(self):
        """Executing the submit_from_local_file method should execute successfully."""
        command_output = self.jobs.submit_from_local_file(SAMPLE_JCL_FIXTURE_PATH)
        jobid = command_output['jobid']
        self.assertIsNotNone(jobid)

    def test_submit_plaintext_should_execute_properly(self):
        """Executing the submit_plaintext method should execute successfully."""
        command_output = self.jobs.submit_plaintext('\n'.join(self.jobs_fixtures_json['TEST_JCL_CODE']))
        jobid = command_output['jobid']
        self.assertIsNotNone(jobid)
