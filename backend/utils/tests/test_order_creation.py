from unittest import TestCase, mock
import unittest

from utils.orders import create_item
import asyncio


class TestCreateItem(TestCase):

    @mock.patch("aiohttp.ClientSession.post")
    @mock.patch("aiohttp.ClientResponse.text")
    @mock.patch("utils.orders.logger.error")
    async def test_create_order_item_success(
        self, mock_logger_error, mock_response_text, mock_session_post
    ):
        """
        Test the create_order_item_success function.

        This function tests the create_order_item_success function by mocking the necessary dependencies and asserting that the function behaves as expected.

        Parameters:
        - mock_logger_error: A mock object representing the logger.error method.
        - mock_response_text: A mock object representing the aiohttp.ClientResponse.text method.
        - mock_session_post: A mock object representing the aiohttp.ClientSession.post method.

        Returns:
        - None
        """
        mock_response_text.return_value = '{"assignee": "h9kVj2@example.com", "name": "Test Order", "clickup_id": "123", "clickup_user_id": "456", "priority": "normal", "status": "in progress", "content": "Test order content"}'
        mock_session_post.return_value.status = 200

        order_data = {
            "assignee": "h9kVj2@example.com",
            "name": "Test Order",
            "clickup_id": "123",
            "clickup_user_id": "456",
            "priority": "normal",
            "status": "in progress",
            "content": "Test order content",
        }
        url = "https://example.com/create"
        item_type = "order_item"

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(create_item(order_data, url, item_type))
        loop.close()

        mock_logger_error.assert_not_called()

    @mock.patch("aiohttp.ClientSession.post")
    @mock.patch("aiohttp.ClientResponse.text")
    @mock.patch("utils.orders.logger.error")
    async def test_create_order_item_non_200_response(
        self, mock_logger_error, mock_response_text, mock_session_post
    ):
        """
        Test the behavior of the create_order_item_non_200_response function when a non-200 response is received.

        Args:
            mock_logger_error (MagicMock): A mock object for the logger.error method.
            mock_response_text (MagicMock): A mock object for the aiohttp.ClientResponse.text method.
            mock_session_post (MagicMock): A mock object for the aiohttp.ClientSession.post method.

        Returns:
            None

        Raises:
            Exception: If the create_item function raises an exception.
        """
        mock_response_text.return_value = "Internal Server Error"
        mock_session_post.return_value.status = 500

        order_data = {
            "assignee": "h9Vj2@example.com",
            "name": "Test Order",
            "clickup_id": "123",
            "clickup_user_id": "456",
            "priority": "normal",
            "status": "in progress",
            "content": "Test order content",
        }
        url = "https://example.com/create"
        item_type = "order_item"

        with self.assertRaises(Exception):
            await create_item(order_data, url, item_type)

        mock_logger_error.assert_called()

    @mock.patch("aiohttp.ClientSession.post")
    @mock.patch("aiohttp.ClientResponse.text")
    @mock.patch("utils.orders.logger.error")
    async def test_create_order_item_exception_decoding_json(
        self, mock_logger_error, mock_response_text, mock_session_post
    ):
        """
        Test the behavior of the create_order_item_exception_decoding_json function when an exception occurs during JSON decoding.

        Parameters:
            - mock_logger_error: A mock object representing the logger.error method.
            - mock_response_text: A mock object representing the aiohttp.ClientResponse.text method.
            - mock_session_post: A mock object representing the aiohttp.ClientSession.post method.

        Returns:
            None
        """
        mock_response_text.return_value = "Invalid JSON Response"
        mock_session_post.return_value.status = 200

        order_data = {"item_name": "Test Order Item"}
        url = "https://example.com/create"
        item_type = "order_item"

        with self.assertRaises(Exception):
            await create_item(order_data, url, item_type)

        mock_logger_error.assert_called()

    @mock.patch("aiohttp.ClientSession.post")
    @mock.patch("aiohttp.ClientResponse.text")
    @mock.patch("utils.orders.logger.error")
    async def create_order_item_200_response(
        self, mock_logger_error, mock_response_text, mock_session_post
    ):
        mock_response_text.return_value = '{"item_id": 123}'
        mock_session_post.return_value.status = 200

        order_data = {
            "assignee": "h9Vj2@example.com",
            "name": "Test Order",
            "clickup_id": "123",
            "clickup_user_id": "456",
            "priority": "normal",
            "status": "in progress",
            "content": "Test order content",
        }
        url = "https://example.com/create"
        item_type = "order_item"

        await create_item(order_data, url, item_type)

        mock_logger_error.assert_not_called()


if __name__ == "__main__":
    unittest.main()
