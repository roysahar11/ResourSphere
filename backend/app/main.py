from fastapi import FastAPI
from endpoints.ec2 import ec2_create

app = FastAPI()

app.include_router(ec2_create.router)

@app.get("/")
async def root():
    return {"message": "ResourSphere"}