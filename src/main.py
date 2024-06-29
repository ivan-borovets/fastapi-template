import uvicorn
from fastapi import FastAPI

from api_v1 import api_v1_router
from core.settings import settings
from core.settings.fastapi_app import create_app

app: FastAPI = create_app()
app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
