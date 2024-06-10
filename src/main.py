from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import init_database
from src.messages.routers import messages_router
from src.users.auth import auth_backend
from src.users.manager import fastapi_users
from src.users.routers import users_router
from src.users.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI()


### MESSAGE ROUTERS ###
app.include_router(messages_router, tags=["messages"])

###


### USERS ROUTES ###
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users/profile",
    tags=["users"],
)

app.include_router(
    users_router,
    tags=["users"]
)
###
