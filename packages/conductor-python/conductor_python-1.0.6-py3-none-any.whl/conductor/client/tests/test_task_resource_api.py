from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.task_resource_api import TaskResourceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestTaskResourceApi(unittest.TestCase):
    """TaskResourceApi unit test stubs"""

    def setUp(self):
        self.api = TaskResourceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_all(self):
        """Test case for all

        Get the details about each queue  # noqa: E501
        """
        pass

    def test_all_verbose(self):
        """Test case for all_verbose

        Get the details about each queue  # noqa: E501
        """
        pass

    def test_batch_poll(self):
        """Test case for batch_poll

        Batch poll for a task of a certain type  # noqa: E501
        """
        pass

    def test_get_all_poll_data(self):
        """Test case for get_all_poll_data

        Get the last poll data for all task types  # noqa: E501
        """
        pass

    def test_get_external_storage_location1(self):
        """Test case for get_external_storage_location1

        Get the external uri where the task payload is to be stored  # noqa: E501
        """
        pass

    def test_get_poll_data(self):
        """Test case for get_poll_data

        Get the last poll data for a given task type  # noqa: E501
        """
        pass

    def test_get_task(self):
        """Test case for get_task

        Get task by Id  # noqa: E501
        """
        pass

    def test_get_task_logs(self):
        """Test case for get_task_logs

        Get Task Execution Logs  # noqa: E501
        """
        pass

    def test_log(self):
        """Test case for log

        Log Task Execution Details  # noqa: E501
        """
        pass

    def test_poll(self):
        """Test case for poll

        Poll for a task of a certain type  # noqa: E501
        """
        pass

    def test_requeue_pending_task(self):
        """Test case for requeue_pending_task

        Requeue pending tasks  # noqa: E501
        """
        pass

    def test_search1(self):
        """Test case for search1

        Search for tasks based in payload and other parameters  # noqa: E501
        """
        pass

    def test_search_v21(self):
        """Test case for search_v21

        Search for tasks based in payload and other parameters  # noqa: E501
        """
        pass

    def test_size(self):
        """Test case for size

        Get Task type queue sizes  # noqa: E501
        """
        pass

    def test_update_task(self):
        """Test case for update_task

        Update a task  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
