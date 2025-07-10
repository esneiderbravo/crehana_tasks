from fastapi import HTTPException

from src.services.task_graphql import (
    create_task_graphql,
    get_task_by_id_graphql,
    update_task_graphql,
    delete_task_graphql,
    assign_task_to_user_graphql,
)


class TaskController:

    @staticmethod
    async def _get_validated_task(task_id: str):
        """
        Validate if a task exists by its ID.
        :param task_id: ID of the task to be validated.
        :return: A JSON response containing the task details if found.
        """
        task_data = await get_task_by_id_graphql(task_id)
        if not task_data or "errors" in task_data:
            raise HTTPException(status_code=404, detail="Task not found or invalid ID.")

        task_data = task_data.get("data", {}).get("taskById", {})
        if not task_data:
            raise HTTPException(status_code=404, detail="Task not found.")
        return task_data

    @staticmethod
    async def create_task(task_data: dict):
        """
        Create a new task.
        :param task_data: Dictionary containing task data with keys 'title', 'priority', 'status', 'completed_percentage', and 'task_list_id'.
        :return: A JSON response containing the created task.
        """
        return await create_task_graphql(task_data)

    @staticmethod
    async def get_task_by_id(task_id: str):
        """
        Fetch a task by its ID.
        :param task_id: ID of the task to be fetched.
        :return: A JSON response containing the task details.
        """
        await TaskController._get_validated_task(task_id)
        return await get_task_by_id_graphql(task_id)

    @staticmethod
    async def update_task(task_id: str, task_data: dict):
        """
        Update an existing task.
        :param task_id: ID of the task to be updated.
        :param task_data: Dictionary containing updated task data.
        :return: A JSON response containing the updated task.
        """
        await TaskController.get_task_by_id(task_id)
        return await update_task_graphql(task_id, task_data)

    @staticmethod
    async def delete_task(task_id: str):
        """
        Delete a task by its ID.
        :param task_id: ID of the task to be deleted.
        :return: A JSON response confirming the deletion.
        """
        await TaskController._get_validated_task(task_id)
        return await delete_task_graphql(task_id)

    @staticmethod
    async def update_task_status(task_id: str, status: str):
        """
        Change the status of a task.
        :param task_id: ID of the task whose status is to be changed.
        :param status: New status for the task.
        :return: A JSON response containing the updated task.
        """
        task_data = await TaskController._get_validated_task(task_id)
        task_data["status"] = status
        return await update_task_graphql(task_id, task_data)

    @staticmethod
    async def assign_task_to_user(task_id: str, user_id: str):
        """
        Assign a task to a user.
        :param task_id: ID of the task to be assigned.
        :param user_id: ID of the user to whom the task is assigned.
        :return: A JSON response containing the updated task with the assigned user.
        """
        await TaskController._get_validated_task(task_id)
        return await assign_task_to_user_graphql(task_id, user_id)
