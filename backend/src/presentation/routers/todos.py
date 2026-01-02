"""Todos router for CRUD operations."""
from fastapi import APIRouter, HTTPException, status
from typing import List

from src.presentation.dependencies import SessionDep, CurrentUserDep
from src.presentation.schemas import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    ErrorResponse
)
from src.application.todos.todo_service import TodoService


router = APIRouter()


@router.get(
    "",
    response_model=List[TodoResponse],
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated"
        }
    }
)
async def get_todos(
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Get all todos for the current user.

    Requires authentication.

    Returns:
    - **todos**: List of todos (ordered by creation date, newest first)
    """
    todo_service = TodoService(session)
    todos = todo_service.get_all_todos(current_user.id)

    return [
        TodoResponse(
            id=todo.id,
            user_id=todo.user_id,
            title=todo.title,
            is_complete=todo.is_complete,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
        for todo in todos
    ]


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Validation error"
        },
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated"
        }
    }
)
async def create_todo(
    request: TodoCreateRequest,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Create a new todo for the current user.

    Requires authentication.

    - **title**: Todo title (max 500 characters)

    Returns:
    - **todo**: Created todo
    """
    todo_service = TodoService(session)

    try:
        todo = todo_service.create_todo(
            user_id=current_user.id,
            title=request.title
        )

        return TodoResponse(
            id=todo.id,
            user_id=todo.user_id,
            title=todo.title,
            is_complete=todo.is_complete,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Todo not found"
        },
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated"
        }
    }
)
async def get_todo(
    todo_id: int,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Get a specific todo by ID.

    Requires authentication.
    Only returns todos belonging to the current user.

    Returns:
    - **todo**: Todo details
    """
    todo_service = TodoService(session)

    try:
        todo = todo_service.get_todo(todo_id, current_user.id)

        return TodoResponse(
            id=todo.id,
            user_id=todo.user_id,
            title=todo.title,
            is_complete=todo.is_complete,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Validation error"
        },
        404: {
            "model": ErrorResponse,
            "description": "Todo not found"
        },
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated"
        }
    }
)
async def update_todo(
    todo_id: int,
    request: TodoUpdateRequest,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Update a todo's title.

    Requires authentication.
    Only updates todos belonging to the current user.

    - **title**: New todo title (max 500 characters)

    Returns:
    - **todo**: Updated todo
    """
    todo_service = TodoService(session)

    try:
        todo = todo_service.update_todo(
            todo_id=todo_id,
            user_id=current_user.id,
            title=request.title
        )

        return TodoResponse(
            id=todo.id,
            user_id=todo.user_id,
            title=todo.title,
            is_complete=todo.is_complete,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )

    except ValueError as e:
        status_code = (
            status.HTTP_404_NOT_FOUND
            if "not found" in str(e).lower()
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=str(e))


@router.patch(
    "/{todo_id}/toggle",
    response_model=TodoResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Todo not found"
        },
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated"
        }
    }
)
async def toggle_todo(
    todo_id: int,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Toggle todo completion status.

    Requires authentication.
    Only toggles todos belonging to the current user.

    Returns:
    - **todo**: Updated todo
    """
    todo_service = TodoService(session)

    try:
        todo = todo_service.toggle_complete(todo_id, current_user.id)

        return TodoResponse(
            id=todo.id,
            user_id=todo.user_id,
            title=todo.title,
            is_complete=todo.is_complete,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Todo not found"
        },
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated"
        }
    }
)
async def delete_todo(
    todo_id: int,
    session: SessionDep,
    current_user: CurrentUserDep
):
    """
    Delete a todo.

    Requires authentication.
    Only deletes todos belonging to the current user.

    Returns:
    - 204 No Content
    """
    todo_service = TodoService(session)

    try:
        todo_service.delete_todo(todo_id, current_user.id)
        return None

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
