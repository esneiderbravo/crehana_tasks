import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from unittest.mock import patch


@pytest.mark.asyncio
class TestTaskListsRouter:

    FAKE_JWT = "Bearer test.jwt.token"
    HEADERS = {"Authorization": FAKE_JWT}

    @patch("src.controllers.task_lists_controller.TaskListController.create_task_list")
    async def test_create_task_list_success(self, mock_create, test_app):
        """
        Test creating a task list successfully.
        """
        mock_create.return_value = {
            "data": {"createTaskList": {"taskList": {"id": "123", "name": "My Tasks"}}}
        }

        payload = {"name": "My Tasks"}
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/task-lists", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"
        assert response.json()["name"] == "My Tasks"

    async def test_create_task_list_empty_name(self, test_app):
        """
        Test creating a task list with an empty name.
        """
        payload = {"name": " "}
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/task-lists", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "name" in response.text

    @patch("src.controllers.task_lists_controller.TaskListController.fetch_task_list_by_id")
    async def test_fetch_task_list_success(self, mock_fetch, test_app):
        """
        Test fetching a task list by ID successfully.
        """
        mock_fetch.return_value = {"data": {"taskListById": {"id": "123", "name": "Work"}}}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/task-lists/123", headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"
        assert response.json()["name"] == "Work"

    @patch("src.controllers.task_lists_controller.TaskListController.update_task_list")
    async def test_update_task_list_success(self, mock_update, test_app):
        mock_update.return_value = {
            "data": {"updateTaskListById": {"taskList": {"id": "123", "name": "Updated"}}}
        }

        payload = {"name": "Updated"}
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.put("/task-lists/123", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated"

    async def test_update_task_list_empty_name(self, test_app):
        payload = {"name": " "}
        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.put("/task-lists/123", json=payload, headers=self.HEADERS)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "name" in response.text

    @patch("src.controllers.task_lists_controller.TaskListController.delete_task_list")
    async def test_delete_task_list_success(self, mock_delete, test_app):
        mock_delete.return_value = {"data": {"deleteTaskListById": {"deletedTaskListId": "123"}}}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete("/task-lists/123", headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Task list deleted successfully."

    @patch("src.controllers.task_lists_controller.TaskListController.delete_task_list")
    async def test_delete_task_list_not_found(self, mock_delete, test_app):
        mock_delete.return_value = {"data": {"deleteTaskListById": {"deletedTaskListId": ""}}}

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.delete("/task-lists/123", headers=self.HEADERS)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.text

    @patch(
        "src.controllers.task_lists_controller.TaskListController.fetch_task_lists_with_tasks_and_filters"
    )
    async def test_fetch_tasks_without_filters(self, mock_fetch, test_app):
        mock_fetch.return_value = {
            "data": {"taskListById": {"id": "123", "name": "My List", "tasks": []}}
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/task-lists/123/tasks", headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == "123"

    @patch(
        "src.controllers.task_lists_controller.TaskListController.fetch_task_lists_with_tasks_and_filters"
    )
    async def test_fetch_tasks_with_filters(self, mock_fetch, test_app):
        mock_fetch.return_value = {
            "data": {"allTasks": {"nodes": [{"id": "t1", "title": "Do something"}]}}
        }

        transport = ASGITransport(app=test_app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/task-lists/123/tasks?status=pending", headers=self.HEADERS)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]["id"] == "t1"
