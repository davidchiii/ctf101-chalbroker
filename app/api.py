from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
import os, time
from app.utils import check_system, find_dockerfiles, run_build
from docker.errors import NotFound, APIError

app = FastAPI()
client = docker.from_env()

paths = find_dockerfiles()

START_TIME = time.time()
@app.get("/")
def root():
    uptime = round(time.time() - START_TIME, 2)
    return {
        "status": "ok",
        "uptime_seconds": uptime
    }

@app.get("/api/challenges")
def list():
    return {"challenges": paths}

class CreateInstanceDataRequest(BaseModel):
    user_id: int | str

# Should be GET because sending a POST request over and over should NOT make more and more instances.
@app.put("/api/challenges/{name}")
def start_instance(name: str, data: CreateInstanceDataRequest):

    if name not in paths:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    chal_path = paths[name]
    container_name = f"{name}-{data.user_id}"
    image_tag = container_name

    try:
        # See if it exists
        try:
            container = client.containers.get(container_name)
            return {
                "status": "ALREADY_RUNNING",
                "name": name,
                "container_id": container.id
            }
        except NotFound:
            pass  # This is expected if it doesn't exist

        # Build image
        image, build_logs = client.images.build(
            path=chal_path, 
            tag=image_tag,
            rm=True
        )
        
        print(f"Image '{image_tag}' built.")
        print(f"Running container '{data.user_id}' from image '{image_tag}'...")
        container = client.containers.run(
            image=image_tag,
            name=container_name,
            detach=True,
            ports={"5000/tcp": None},  # expose dynamically
            environment={"USER_ID": data.user_id}
        )
        return {
            "status": "STARTED",
            "name": name,
            "container_id": container.id
        }

    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))

