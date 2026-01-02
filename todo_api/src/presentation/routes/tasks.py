"""Task endpoints - Protected by authentication."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.application.task_service import TaskService
from src.domain.user import User
from src.presentation.dependencies import get_task_service, get_current_user
from src.presentation.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Create a new task for the current user.

    Args:
        task_data: Task creation data.
        current_user: Authenticated user from dependency.
        service: Task service from dependency.

    Returns:
        Created task data.
    """
    task = service.create_task(task_data.title, current_user.id)
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
) -> list[TaskResponse]:
    """Get all tasks for the current user.

    Args:
        current_user: Authenticated user from dependency.
        service: Task service from dependency.

    Returns:
        List of user's tasks.
    """
    tasks = service.get_all_tasks(current_user.id)
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            is_complete=t.is_complete,
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Get a task by ID for the current user.

    Args:
        task_id: ID of task to retrieve.
        current_user: Authenticated user from dependency.
        service: Task service from dependency.

    Returns:
        Task data.

    Raises:
        HTTPException: 404 if task not found or not owned by user.
    """
    task = service.get_task(task_id, current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Update a task's title for the current user.

    Args:
        task_id: ID of task to update.
        task_data: Task update data.
        current_user: Authenticated user from dependency.
        service: Task service from dependency.

    Returns:
        Updated task data.

    Raises:
        HTTPException: 404 if task not found or not owned by user.
    """
    task = service.update_task(task_id, task_data.title, current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
) -> Response:
    """Delete a task for the current user.

    Args:
        task_id: ID of task to delete.
        current_user: Authenticated user from dependency.
        service: Task service from dependency.

    Returns:
        Empty response on success.

    Raises:
        HTTPException: 404 if task not found or not owned by user.
    """
    deleted = service.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Toggle a task's completion status for the current user.

    Args:
        task_id: ID of task to toggle.
        current_user: Authenticated user from dependency.
        service: Task service from dependency.

    Returns:
        Updated task data.

    Raises:
        HTTPException: 404 if task not found or not owned by user.
    """
    task = service.toggle_task_complete(task_id, current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
