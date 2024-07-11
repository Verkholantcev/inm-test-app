import os
import json
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Эта функция будет выполнена при запуске приложения."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", "users.json")
    with open(file_path, 'w') as f:
        json.dump([], f)
    yield
    os.remove(file_path)


app = FastAPI(lifespan=lifespan)
app.include_router(users_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
