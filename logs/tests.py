from django.test import TestCase

# Create your tests here.
from unittest.mock import patch
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse


class CreateUserViewTest(TestCase):
    @patch("logs.views.log_to_kafka")
    def test_create_user_kafka_logging(self, mock_log_to_kafka):
        client = APIClient()
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
        }
        response = client.post(reverse("create_user"), data, format="json")

        # Verify that log_to_kafka was called
        self.assertTrue(mock_log_to_kafka.called)
        # Check log data if needed
        log_data = mock_log_to_kafka.call_args[0][0]
        self.assertEqual(log_data["message"], "User 'testuser' created successfully.")
