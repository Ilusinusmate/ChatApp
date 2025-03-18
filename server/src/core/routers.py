from core.setup import app
from controllers import routers_list

for router in routers_list:
    app.include_router(router)