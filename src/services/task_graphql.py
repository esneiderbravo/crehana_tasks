from src.infrastructure.graphql_client import execute_graphql


async def create_task_graphql(
    task_data: dict,
):
    """
    Create a new task using GraphQL.
    :param task_data: Dictionary containing task data with keys
    'name', 'description', 'due_date', and 'task_list_id'.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation CreateTask {
            createTask(input: {
                task: {
                    title: "$title",
                    priority: $priority,
                    status: $status,
                    completedPercentage: $completed_percentage
                    taskListId: "$taskListId"
                }
            }) {
                task {
                    id
                    title
                    priority
                    status
                    completedPercentage
                    createdAt
                }
            }
        }
    """
    variables = {
        "title": task_data.get("title"),
        "priority": task_data.get("priority", "medium"),
        "status": task_data.get("status", "pending"),
        "completed_percentage": task_data.get("completed_percentage", 0),
        "taskListId": task_data.get("task_list_id"),
    }

    return await execute_graphql(query, variables)


async def get_task_by_id_graphql(task_id: str):
    """
    Fetch a task by its ID using GraphQL.
    :param task_id: ID of the task to be fetched.
    :return: Result of the GraphQL query containing the task details.
    """
    query = """
        query FetchTaskById {
            taskById(id: "$id") {
                id
                title
                priority
                status
                completedPercentage
                createdAt
            }
        }
    """
    return await execute_graphql(query, {"id": task_id})


async def update_task_graphql(task_id: str, task_data: dict):
    """
    Update an existing task using GraphQL.
    :param task_id: ID of the task to be updated.
    :param task_data: Dictionary containing the updated task data.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation UpdateTask {
            updateTaskById(input: {
                id: "$id",
                taskPatch: {
                    title: "$title",
                    priority: $priority,
                    status: $status,
                    completedPercentage: $completed_percentage
                }
            }) {
                task {
                    id
                    title
                    priority
                    status
                    completedPercentage
                    createdAt
                }
            }
        }
    """
    variables = {
        "id": task_id,
        "title": task_data.get("title"),
        "priority": task_data.get("priority", "medium"),
        "status": task_data.get("status", "pending"),
        "completed_percentage": task_data.get("completed_percentage", 0),
    }

    return await execute_graphql(query, variables)


async def delete_task_graphql(task_id: str):
    """
    Delete a task by its ID using GraphQL.
    :param task_id: ID of the task to be deleted.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation DeleteTask {
            deleteTaskById(input: { id: "$id" }) {
                deletedTaskId
            }
        }
    """
    return await execute_graphql(query, {"id": task_id})


async def assign_task_to_user_graphql(task_id: str, user_id: str):
    """
    Assign a task to a user using GraphQL.
    :param task_id: ID of the task to be assigned.
    :param user_id: ID of the user to whom the task will be assigned.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation createAssignedTask {
            createAssignedTask(
                input: {
                    assignedTask: {
                        taskId: "$taskId",
                        userId: "$userId"
                    }
                }
            ) {
                assignedTask {
                    taskByTaskId {
                        id
                        title
                        priority
                        status
                        completedPercentage
                        createdAt
                    }
                }
            }
        }
    """
    variables = {"taskId": task_id, "userId": user_id}
    return await execute_graphql(query, variables)
