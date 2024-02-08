import uvicorn

from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings
from core.database import engine
from core.database import Base

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def hello():
    return "Hello"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
