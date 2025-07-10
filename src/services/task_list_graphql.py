from src.infrastructure.graphql_client import execute_graphql


async def create_task_list_graphql(name: str):
    """
    Create a new task list using GraphQL.
    :param name: Name of the task list to be created.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation CreateTaskList {
            createTaskList(input: {
                taskList: {
                    name: "$name"
                }
            }) {
                taskList {
                    id
                    name
                    createdAt
                }
            }
        }
    """
    variables = {"name": name}
    return await execute_graphql(query, variables)


async def get_task_lists_by_id_graphql(task_list_id: str):
    """
    Fetch a task list by its ID using GraphQL.
    :param task_list_id: ID of the task list to be fetched.
    :return: Result of the GraphQL query containing the task list and its tasks.
    """
    query = """
        query FetchTaskListById {
            taskListById(id: "$id") {
                id
                name
                createdAt
            }
        }
    """
    return await execute_graphql(query, {"id": task_list_id})


async def update_task_list_graphql(task_list_id: str, name: str):
    """
    Update an existing task list using GraphQL.
    :param task_list_id: ID of the task list to be updated.
    :param name: New name for the task list.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation UpdateTaskList {
            updateTaskListById(input: {
                id: "$id",
                taskListPatch: {
                    name: "$name"
                }
            }) {
                taskList {
                    id
                    name
                    createdAt
                }
            }
        }
    """
    variables = {"id": task_list_id, "name": name}
    return await execute_graphql(query, variables)


async def delete_task_list_graphql(task_list_id: str):
    """
    Delete a task list by its ID using GraphQL.
    :param task_list_id: ID of the task list to be deleted.
    :return: Result of the GraphQL mutation.
    """
    query = """
        mutation DeleteTaskList {
            deleteTaskListById(input: {
                id: "$id"
            }) {
                deletedTaskListId
            }
        }
    """
    return await execute_graphql(query, {"id": task_list_id})


async def get_task_list_with_task_with_filters_graphql(
    task_list_id: str, filters: dict = None
):
    """
    Fetch a task list along with its tasks by the task list ID using GraphQL.
    :param task_list_id: ID of the task list to be fetched.
    :param filters: Optional filters to apply to the task list.
    :return: Result of the GraphQL query containing the task list and its tasks.
    """
    query = """
        query FetchTaskListWithTasks {
            taskListById(id: "$id") {
                id
                name
                createdAt
                tasksByTaskListId {
                    nodes {
                        id
                        status
                        priority
                        title
                        completedPercentage
                        createdAt
                    }
                }
            }
        }
    """
    if filters:
        query = """
            query allTasksByFilter {
                allTasks(condition: { priority: $priority, status: $status, taskListId: "$id" }) {
                    nodes {
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
            "id": task_list_id,
            "priority": filters.get("priority"),
            "status": filters.get("status"),
        }
        return await execute_graphql(query, variables)

    return await execute_graphql(query, {"id": task_list_id})
