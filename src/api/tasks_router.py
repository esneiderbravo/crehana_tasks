from fastapi import APIRouter, HTTPException, Request

from src.application.auth import require_authentication
from src.controllers.task_controller import TaskController

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", summary="Create a new task")
@require_authentication
async def create_task(request: Request, current_user: dict = None):
    """
    Create a new task.
    :param request: The HTTP request containing the task data.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the created task.
    """
    try:
        task_data = await request.json()

        result = await TaskController.create_task(task_data)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["createTask"]["task"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", summary="Fetch a task by ID")
@require_authentication
async def get_task_by_id(task_id: str, request: Request, current_user: dict = None):
    """
    Fetch a task by its ID.
    :param task_id: ID of the task to be fetched.
    :param request: The HTTP request.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the task details.
    """
    try:
        result = await TaskController.get_task_by_id(task_id)

        if "errors" in result:
            raise HTTPException(status_code=404, detail=result["errors"])

        return result["data"]["taskById"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_id}", summary="Update an existing task")
@require_authentication
async def update_task(task_id: str, request: Request, current_user: dict = None):
    """
    Update an existing task.
    :param task_id: ID of the task to be updated.
    :param request: The HTTP request containing the updated task data.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the updated task.
    """
    try:
        task_data = await request.json()

        result = await TaskController.update_task(task_id, task_data)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["updateTaskById"]["task"]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}", summary="Delete a task by ID")
@require_authentication
async def delete_task(task_id: str, request: Request, current_user: dict = None):
    """
    Delete a task by its ID.
    :param task_id: ID of the task to be deleted.
    :param request: The HTTP request.
    :param current_user: The currently authenticated user.
    :return: A JSON response indicating the deletion status.
    """
    try:
        result = await TaskController.delete_task(task_id)

        if "errors" in result:
            raise HTTPException(status_code=404, detail=result["errors"])

        if not result.get("data", {}).get("deleteTaskById", {}).get("deletedTaskId", ""):
            raise HTTPException(status_code=404, detail="Task list not found or already deleted.")

        return {"message": "Task deleted successfully."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{task_id}/status", summary="Update task status")
@require_authentication
async def update_task_status(task_id: str, request: Request, current_user: dict = None):
    """
    Update the status of a task.
    :param task_id: ID of the task to be updated.
    :param request: The HTTP request containing the new status.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the updated task.
    """
    try:
        status_data = await request.json()
        status = status_data.get("status")

        result = await TaskController.update_task_status(task_id, status)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["updateTaskById"]["task"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assign", summary="Assign task to user")
@require_authentication
async def assign_task_to_user(request: Request, current_user: dict = None):
    """
    Assign a task to a user.
    :param request: The HTTP request containing the user ID.
    :param current_user: The currently authenticated user.
    :return: A JSON response containing the updated task.
    """
    try:
        assign_task_data = await request.json()
        task_id = assign_task_data.get("task_id")
        user_id = assign_task_data.get("user_id")

        result = await TaskController.assign_task_to_user(task_id, user_id)

        if "errors" in result:
            raise HTTPException(status_code=400, detail=result["errors"])

        return result["data"]["createAssignedTask"]["assignedTask"]["taskByTaskId"]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
