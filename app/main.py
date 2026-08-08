from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis
import time
import os

app = FastAPI()
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True
)
with open("app/token_bucket.lua", "r") as file:
    lua_script = file.read()

BUCKET_SIZE = 5   
REFILL_RATE = 0.1     


@app.middleware("http")
async def rate_limiter(request: Request, call_next):

    ip = request.client.host
    current_time = time.time()

    allowed = redis_client.eval(
        lua_script,
        2,
        f"{ip}:tokens",
        f"{ip}:last_time",
        BUCKET_SIZE,
        REFILL_RATE,
        current_time,
    )

    if allowed == 0:
        return JSONResponse(
            status_code=429,
            content={"message": "Too Many Requests"}
        )

    response = await call_next(request)
    return response


@app.get("/")
def home():
    return {
        "message": "Welcome to Distributed Rate Limiter"
    }