from handlers.auth import router as auth_router
from handlers.tasks import router as tasks_router
from handlers.users import router as users_router

routers = [tasks_router, users_router, auth_router]
