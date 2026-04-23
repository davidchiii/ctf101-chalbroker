from fastapi import FastAPI
import os, time
from app.utils import check_system, find_dockerfiles, run_build

app = FastAPI()

paths = find_dockerfiles()

START_TIME = time.time()
@app.get("/")
def root():
    uptime = round(time.time() - START_TIME, 2)
    return {
        "status": "ok",
        "uptime_seconds": uptime
    }

@app.get("/api/challenge")
def list():
    return {"challenges": paths}

@app.get("/api/challenge/{chal_name}")
def start_instance(chal_name: str):
    return {"chal_name": chal_name}


def create_challenge(name: str, userid: int):
    flag = challenge_dict[name]