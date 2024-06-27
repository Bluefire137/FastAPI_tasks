from fastapi import FastAPI, Depends


from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend
from database import User
from auth.manager import get_user_manager
from auth.auth_schemas import UserRead, UserCreate
from tasks.router import router as router_task

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Войти"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Зарегистрироваться"],
)

app.include_router(router_task)

current_user = fastapi_users.current_user()


@app.get("/protected-route", tags=["Защищенный вход"])
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route", tags=["Незащищенный вход"])
def unprotected_route():
    return f"Hello, anonym"
