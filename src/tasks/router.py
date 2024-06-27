from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_async_session
from tasks.models import Task

router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


@router.get("/")
async def get_specific_tasks(task_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.c.type == task_type)
    result = await session.execute(query)
    return
