from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis

app = FastAPI()
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

LIMIT = 5


@app.middleware("http")
async def rate_limiter(request: Request, call_next):

    ip = request.client.host

    count = redis_client.incr(ip)
    if count == 1:
        redis_client.expire(ip, 60)
    print(f"{ip} -> {count}")

    if count > LIMIT:
        return JSONResponse(
            status_code=429,
            content={"message": "Too Many Requests"}
        )

    response = await call_next(request)

    return response


@app.get("/")
def home():
    return {"message": "Welcome to Distributed Rate Limiter"} 