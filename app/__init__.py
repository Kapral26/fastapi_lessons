from app.users.users_profile.handlers import router as user_routers
from app.users.auth.handlers import router as auth_routers
from app.tasks.handlers import router as task_routers

all_routers = [
    user_routers,
    auth_routers,
    task_routers
]
