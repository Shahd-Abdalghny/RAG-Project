from fastapi import FastAPI
app = FastAPI()

@app.get("/Welcome")
def welcome_message():
    return {"message": "Welcome to mini-RAG!"}