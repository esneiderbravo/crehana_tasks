from fastapi import HTTPException

from src.services.task_list_graphql import (
    create_task_list_graphql,
    get_task_lists_by_id_graphql,
    update_task_list_graphql,
    delete_task_list_graphql,
    get_task_list_with_task_with_filters_graphql,
)


class TaskListController:

    @staticmethod
    async def _get_validated_task_list(task_list_id: str):
        """
        Validate the existence of a task list by its ID.
        :param task_list_id: ID of the task list to be validated.
        :return: A JSON response containing the task list if it exists.
        """
        task_list_data = await get_task_lists_by_id_graphql(task_list_id)
        if not task_list_data or "errors" in task_list_data:
            raise HTTPException(status_code=404, detail="Task list not found or invalid ID.")

        task_list_data = task_list_data.get("data", {}).get("taskListById", {})
        if not task_list_data:
            raise HTTPException(status_code=404, detail="Task list not found.")
        return task_list_data

    @staticmethod
    async def create_task_list(name: str):
        """
        Create a new task list.
        :param name: Name of the task list to be created.
        :return: A JSON response containing the created task list.
        """
        return await create_task_list_graphql(name)

    @staticmethod
    async def fetch_task_list_by_id(task_list_id: str):
        """
        Fetch a task list by its ID.
        :param task_list_id: ID of the task list to be fetched.
        :return: A JSON response containing the task list and its tasks.
        """
        await TaskListController._get_validated_task_list(task_list_id)
        return await get_task_lists_by_id_graphql(task_list_id)

    @staticmethod
    async def update_task_list(task_list_id: str, name: str):
        """
        Update an existing task list.
        :param task_list_id: ID of the task list to be updated.
        :param name: New name for the task list.
        :return: A JSON response containing the updated task list.
        """
        await TaskListController._get_validated_task_list(task_list_id)
        return await update_task_list_graphql(task_list_id, name)

    @staticmethod
    async def delete_task_list(task_list_id: str):
        """
        Delete a task list by its ID.
        :param task_list_id: ID of the task list to be deleted.
        :return: A JSON response indicating success or failure.
        """
        await TaskListController._get_validated_task_list(task_list_id)
        return await delete_task_list_graphql(task_list_id)

    @staticmethod
    async def fetch_task_lists_with_tasks_and_filters(task_list_id: str, filters: dict = None):
        """
        Fetch all task lists with their tasks.
        :param task_list_id: ID of the task list to fetch tasks for.
        :param filters: Optional filters to apply to the task list.
        :return: A JSON response containing the task list and its tasks.
        """
        await TaskListController._get_validated_task_list(task_list_id)
        return await get_task_list_with_task_with_filters_graphql(task_list_id, filters)
