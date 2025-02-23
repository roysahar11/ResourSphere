from fastapi import FastAPI
from app.endpoints.ec2 import ec2_create
from app.endpoints.auth import login
import uvicorn

app = FastAPI()

app.include_router(ec2_create.router)
app.include_router(login.router)
@app.get("/")
async def root():
    return {"message": "ResourSphere"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)