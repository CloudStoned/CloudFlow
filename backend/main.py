import uvicorn
from fastapi import FastAPI
from services.gmail_service import test_gmail_connection

app = FastAPI()

@app.get("/gmail/test/{user_id}")
def gmail_test(user_id: str):
    return test_gmail_connection(user_id)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)