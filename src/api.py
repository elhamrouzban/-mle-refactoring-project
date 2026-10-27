from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "House Price API is running"}