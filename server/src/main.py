import uvicorn

from core.setup import app
from core.settings import *
from core.routers import *
from core.db import *


def run_app():
    uvicorn.run(
        app,
        host=HOST,
        port=PORT
    )

if __name__ == "__main__":
    run_app()