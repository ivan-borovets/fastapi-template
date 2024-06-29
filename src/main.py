import uvicorn
from fastapi import FastAPI

from core.settings.app_factory import create_app
from core.settings.settings import settings

app: FastAPI = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
