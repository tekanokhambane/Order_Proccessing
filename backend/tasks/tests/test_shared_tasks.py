import unittest
from unittest.mock import patch, AsyncMock

import asyncio

from tasks.tasks import process_task

TASK_URL = "https://hook.eu2.make.com/some-url"


class TestProcessTask(unittest.TestCase):
    @patch("utils.orders.update_clickup_task", new_callable=AsyncMock)
    async def test_process_task(self, mock_update_task):
        """
        Test the process_task function by mocking the update_clickup_task and asserting its call.
        """
        order = "test_order"
        await process_task(order)
        mock_update_task.assert_called_once_with(order, TASK_URL)


if __name__ == "__main__":
    unittest.main()
