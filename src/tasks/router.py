from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from database import get_async_session
from tasks.models import Task
from tasks.schema import TaskCreate

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


@router.get("/")
async def get_specific_tasks(task_type: str = Query(...), session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Task).where(Task.type == task_type)
        result = await session.execute(query)
        tasks = result.scalars().all()
        return {"status": "success", "data": tasks}
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/")
async def add_specific_task(new_task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Task).values(**new_task.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "message": "Task added successfully"}
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
