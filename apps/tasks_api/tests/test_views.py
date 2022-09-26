from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestTaskViewSet(APITestCase):
    def test_create_successfully_task(self):
        add_url = reverse("task-add")
        data = {
            "title": "Task test",
            "description": "test 1234567890",
            "completed": False
        }
        response = self.client.post(add_url, data=data, format="json")

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)

    def test_update_successfully_task(self):
        pass

    def test_partial_update_successfully_task(self):
        pass

    def test_list_successfully_tasks(self):
        pass

    def test_retrieve_successfully_task(self):
        pass

    def test_delete_successfully_task(self):
        pass
