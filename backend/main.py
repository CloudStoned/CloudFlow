import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, emails, actions
from core.config import get_settings

app = FastAPI()
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Cloudflow API"}


app.include_router(auth.router)
app.include_router(emails.router)
app.include_router(actions.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)