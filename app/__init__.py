from app.users.users_profile import user_routers
from app.users.auth import auth_routers
from app.tasks import task_routers

all_routers = [user_routers, auth_routers, task_routers]
