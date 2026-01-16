from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Debug App is Working!"}
