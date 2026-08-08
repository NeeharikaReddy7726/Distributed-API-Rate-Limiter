import requests
from concurrent.futures import ThreadPoolExecutor

URLS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002"
]

def send_request(i):
    url = URLS[i % len(URLS)]
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        return str(e)

with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(send_request, range(50)))

print("200 OK:", results.count(200))
print("429 Too Many Requests:", results.count(429))
