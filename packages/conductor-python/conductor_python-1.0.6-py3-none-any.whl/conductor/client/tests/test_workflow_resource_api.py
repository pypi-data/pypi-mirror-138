from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.workflow_resource_api import WorkflowResourceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestWorkflowResourceApi(unittest.TestCase):
    """WorkflowResourceApi unit test stubs"""

    def setUp(self):
        self.api = WorkflowResourceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_decide(self):
        """Test case for decide

        Starts the decision task for a workflow  # noqa: E501
        """
        pass

    def test_delete(self):
        """Test case for delete

        Removes the workflow from the system  # noqa: E501
        """
        pass

    def test_get_execution_status(self):
        """Test case for get_execution_status

        Gets the workflow by workflow id  # noqa: E501
        """
        pass

    def test_get_external_storage_location(self):
        """Test case for get_external_storage_location

        Get the uri and path of the external storage where the workflow payload is to be stored  # noqa: E501
        """
        pass

    def test_get_running_workflow(self):
        """Test case for get_running_workflow

        Retrieve all the running workflows  # noqa: E501
        """
        pass

    def test_get_workflows(self):
        """Test case for get_workflows

        Lists workflows for the given correlation id list  # noqa: E501
        """
        pass

    def test_get_workflows1(self):
        """Test case for get_workflows1

        Lists workflows for the given correlation id  # noqa: E501
        """
        pass

    def test_pause_workflow(self):
        """Test case for pause_workflow

        Pauses the workflow  # noqa: E501
        """
        pass

    def test_rerun(self):
        """Test case for rerun

        Reruns the workflow from a specific task  # noqa: E501
        """
        pass

    def test_reset_workflow(self):
        """Test case for reset_workflow

        Resets callback times of all non-terminal SIMPLE tasks to 0  # noqa: E501
        """
        pass

    def test_restart(self):
        """Test case for restart

        Restarts a completed workflow  # noqa: E501
        """
        pass

    def test_resume_workflow(self):
        """Test case for resume_workflow

        Resumes the workflow  # noqa: E501
        """
        pass

    def test_retry(self):
        """Test case for retry

        Retries the last failed task  # noqa: E501
        """
        pass

    def test_search(self):
        """Test case for search

        Search for workflows based on payload and other parameters  # noqa: E501
        """
        pass

    def test_search_v2(self):
        """Test case for search_v2

        Search for workflows based on payload and other parameters  # noqa: E501
        """
        pass

    def test_search_workflows_by_tasks(self):
        """Test case for search_workflows_by_tasks

        Search for workflows based on task parameters  # noqa: E501
        """
        pass

    def test_search_workflows_by_tasks_v2(self):
        """Test case for search_workflows_by_tasks_v2

        Search for workflows based on task parameters  # noqa: E501
        """
        pass

    def test_skip_task_from_workflow(self):
        """Test case for skip_task_from_workflow

        Skips a given task from a current running workflow  # noqa: E501
        """
        pass

    def test_start_workflow(self):
        """Test case for start_workflow

        Start a new workflow. Returns the ID of the workflow instance that can be later used for tracking  # noqa: E501
        """
        pass

    def test_start_workflow1(self):
        """Test case for start_workflow1

        Start a new workflow with StartWorkflowRequest, which allows task to be executed in a domain  # noqa: E501
        """
        pass

    def test_terminate1(self):
        """Test case for terminate1

        Terminate workflow execution  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
