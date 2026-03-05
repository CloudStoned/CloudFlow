import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import gmail
from core.logger import get_logger


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = get_logger(__name__)

app.include_router(gmail.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)