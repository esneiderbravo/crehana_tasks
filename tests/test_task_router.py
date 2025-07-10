import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from unittest.mock import patch


@pytest.mark.asyncio
class TestTasksRouter:

    FAKE_JWT = "Bearer test.jwt.token"
    HEADERS = {"Authorization": FAKE_JWT}

    @patch("src.controllers.task_controller.TaskController.create_task")
    async def test_create_task_success(self, mock_create, test_app):
        mock_create.return_value = {
            "data": {
                "createTask": {
                    "task": {
                        "id": "123",
                        "title": "New Task",
                        "priority": "medium",
                        "status": "pending",
                        "completedPercentage": 0,
                        "createdAt": "2023-01-01T00:00:00Z",
                    }
                }
            }
        }

        payload = {
            "title": "New Task",
            "priority": "medium",
            "status": "pending",
            "completed_percentage": 0,
            "task_list_id": "list-123",
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/tasks", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"
        assert response.json()["title"] == "New Task"

    @patch("src.controllers.task_controller.TaskController.create_task")
    async def test_create_task_error(self, mock_create, test_app):
        mock_create.return_value = {"errors": ["Invalid task data"]}

        payload = {"title": "New Task", "task_list_id": "list-123"}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/tasks", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid task data" in response.text

    @patch("src.controllers.task_controller.TaskController.get_task_by_id")
    async def test_get_task_by_id_success(self, mock_get, test_app):
        mock_get.return_value = {
            "data": {
                "taskById": {
                    "id": "123",
                    "title": "Example Task",
                    "priority": "high",
                    "status": "in_progress",
                    "completedPercentage": 50,
                    "createdAt": "2023-01-01T00:00:00Z",
                }
            }
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/tasks/123", headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"
        assert response.json()["title"] == "Example Task"
        assert response.json()["completedPercentage"] == 50

    @patch("src.controllers.task_controller.TaskController.get_task_by_id")
    async def test_get_task_by_id_not_found(self, mock_get, test_app):
        mock_get.return_value = {"errors": ["Task not found"]}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/tasks/999", headers=self.HEADERS)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Task not found" in response.text

    @patch("src.controllers.task_controller.TaskController.update_task")
    async def test_update_task_success(self, mock_update, test_app):
        mock_update.return_value = {
            "data": {
                "updateTaskById": {
                    "task": {
                        "id": "123",
                        "title": "Updated Task",
                        "priority": "high",
                        "status": "in_progress",
                        "completedPercentage": 75,
                        "createdAt": "2023-01-01T00:00:00Z",
                    }
                }
            }
        }

        payload = {
            "title": "Updated Task",
            "priority": "high",
            "status": "in_progress",
            "completed_percentage": 75,
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.put("/tasks/123", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Updated Task"
        assert response.json()["completedPercentage"] == 75

    @patch("src.controllers.task_controller.TaskController.delete_task")
    async def test_delete_task_success(self, mock_delete, test_app):
        mock_delete.return_value = {"data": {"deleteTaskById": {"deletedTaskId": "123"}}}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete("/tasks/123", headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Task deleted successfully."

    @patch("src.controllers.task_controller.TaskController.delete_task")
    async def test_delete_task_not_found(self, mock_delete, test_app):
        mock_delete.return_value = {"data": {"deleteTaskById": {"deletedTaskId": ""}}}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete("/tasks/999", headers=self.HEADERS)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.text

    @patch("src.controllers.task_controller.TaskController.update_task_status")
    async def test_update_task_status_success(self, mock_status, test_app):
        mock_status.return_value = {
            "data": {
                "updateTaskById": {
                    "task": {
                        "id": "123",
                        "title": "Task",
                        "priority": "medium",
                        "status": "completed",
                        "completedPercentage": 100,
                        "createdAt": "2023-01-01T00:00:00Z",
                    }
                }
            }
        }

        payload = {"status": "completed"}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.put("/tasks/123/status", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "completed"

    @patch("src.controllers.task_controller.TaskController.assign_task_to_user")
    async def test_assign_task_to_user_success(self, mock_assign, test_app):
        mock_assign.return_value = {
            "data": {
                "createAssignedTask": {
                    "assignedTask": {
                        "taskByTaskId": {
                            "id": "123",
                            "title": "Assigned Task",
                            "priority": "medium",
                            "status": "pending",
                            "completedPercentage": 0,
                            "createdAt": "2023-01-01T00:00:00Z",
                        }
                    }
                }
            }
        }

        payload = {"task_id": "123", "user_id": "user-456"}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/tasks/assign", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"
        assert response.json()["title"] == "Assigned Task"

    @patch("src.controllers.task_controller.TaskController.assign_task_to_user")
    async def test_assign_task_to_user_error(self, mock_assign, test_app):
        mock_assign.return_value = {"errors": ["Task or user not found"]}

        payload = {"task_id": "123", "user_id": "invalid-user"}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/tasks/assign", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Task or user not found" in response.text
