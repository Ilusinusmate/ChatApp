from fastapi import APIRouter
from .messages import router as message_router
from .auth import router as auth_router
from .users import router as users_router
from .groups import router as groups_router

routers_list: list[APIRouter] = [
    message_router,
    auth_router,
    users_router,
    groups_router
]


