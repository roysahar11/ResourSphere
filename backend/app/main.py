from fastapi import FastAPI
from app.endpoints.ec2 import (
    ec2_create, ec2_list, ec2_delete, ec2_start, ec2_stop
)
from app.endpoints.auth import login
from app.endpoints.s3 import s3_create, s3_list, s3_delete
import uvicorn


app = FastAPI()

app.include_router(ec2_create.router)
app.include_router(login.router)
app.include_router(ec2_list.router)
app.include_router(ec2_delete.router)
app.include_router(ec2_start.router)
app.include_router(ec2_stop.router)
app.include_router(s3_create.router)
app.include_router(s3_list.router)
app.include_router(s3_delete.router)


@app.get("/")
async def root():
    return {"message": "ResourSphere"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)