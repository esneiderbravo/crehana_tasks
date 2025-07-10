from fastapi import APIRouter, HTTPException, Path, Request

from src.application.auth import require_authentication
from src.controllers.task_lists_controller import TaskListController

router = APIRouter(prefix="/task-lists", tags=["Task Lists"])


@router.post("", summary="Create a new task list")
@require_authentication
async def create_task_list(request: Request, current_user: dict = None):
    """
    Create a new task list.
    :param request: Request object containing the JSON body with the task list name.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the created task list or an error message.
    """
    try:
        body = await request.json()
        name = body.get("name")

        if not name or not name.strip():
            raise HTTPException(
                status_code=422,
                detail="The 'name' field is required and must not be empty.",
            )

        result = await TaskListController.create_task_list(name)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["createTaskList"]["taskList"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_list_id}", summary="Fetch a task list by ID")
@require_authentication
async def fetch_task_list_by_id(
    request: Request,
    task_list_id: str = Path(..., description="ID of the task list to be fetched"),
    current_user: dict = None,
):
    """
    Fetch a task list by its ID.
    :param request: Request object containing the task list ID.
    :param task_list_id: ID of the task list to be fetched.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the task list and its tasks or an error message.
    """
    try:
        result = await TaskListController.fetch_task_list_by_id(task_list_id)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["taskListById"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_list_id}", summary="Update an existing task list")
@require_authentication
async def update_task_list(
    request: Request,
    task_list_id: str = Path(..., description="ID of the task list to be updated"),
    current_user: dict = None,
):
    """
    Update an existing task list.
    :param task_list_id: ID of the task list to be updated.
    :param request: Request object containing the JSON body with the new name for the task list.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the updated task list or an error message.
    """
    try:
        body = await request.json()
        name = body.get("name")

        if not name or not name.strip():
            raise HTTPException(
                status_code=422,
                detail="The 'name' field is required and must not be empty.",
            )

        result = await TaskListController.update_task_list(task_list_id, name)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["updateTaskListById"]["taskList"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_list_id}", summary="Delete a task list by ID")
@require_authentication
async def delete_task_list(
    request: Request,
    task_list_id: str = Path(..., description="ID of the task list to be deleted"),
    current_user: dict = None,
):
    """
    Delete a task list by its ID.
    :param request: Request object containing the task list ID.
    :param task_list_id: ID of the task list to be deleted.
    :param current_user: The currently authenticated user.
    :return: A JSON response indicating success or failure.
    """
    try:
        result = await TaskListController.delete_task_list(task_list_id)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        if not result.get("data", {}).get("deleteTaskListById", {}).get("deletedTaskListId", ""):
            raise HTTPException(status_code=404, detail="Task list not found or already deleted.")

        return {"message": "Task list deleted successfully."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_list_id}/tasks", summary="Fetch all task lists")
@require_authentication
async def fetch_task_lists_with_tasks(
    request: Request,
    task_list_id: str = Path(..., description="ID of the task list to fetch tasks for"),
    filters: dict = None,
    current_user: dict = None,
):
    """
    Fetch all tasks in a specific task list.
    :param request: Request object containing the task list ID.
    :param task_list_id: ID of the task list to fetch tasks for.
    :param current_user: The currently authenticated user.
    :param filters: Optional filters to apply to the task list.
    :return: A JSON response containing the tasks in the specified task list or an error message.
    """
    try:
        filters = dict(request.query_params)

        result = await TaskListController.fetch_task_lists_with_tasks_and_filters(
            task_list_id, filters
        )

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        if filters:
            return result["data"]["allTasks"]["nodes"]

        return result["data"]["taskListById"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
