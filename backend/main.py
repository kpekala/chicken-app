from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import requests
import urllib.parse
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stores")
def get_stores():
    query = """[out:json][timeout:25];(node["shop"="supermarket"](50.0,19.8,50.1,20.1);way["shop"="supermarket"](50.0,19.8,50.1,20.1););out center;"""
    response = requests.post(
        "https://overpass-api.de/api/interpreter",
        data={"data": query},
        timeout=30
    )
    print("Status:", response.status_code)
    print("Body:", response.text[:500])
    print(urllib.parse.urlencode({"data": query}))
    return response.json()