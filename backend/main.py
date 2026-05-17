import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

#uvicorn main:app --reload
#venv\Scripts\activate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Shop(BaseModel):
    id: int
    name: str
    lat: float
    lng: float

MOCK_SHOPS: list[Shop] = []

def init_shops():
    with open("shops.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for element in data["elements"]:
        tags = element.get("tags", {})
        brand = tags.get("brand") or tags.get("name")
        
        if not brand:
            continue

        # nodes have lat/lon directly, ways have a center object
        if element["type"] == "node":
            lat = element["lat"]
            lng = element["lon"]
        elif element["type"] == "way":
            center = element.get("center", {})
            lat = center.get("lat")
            lng = center.get("lon")
        else:
            continue

        if lat is None or lng is None:
            continue

        MOCK_SHOPS.append(Shop(
            id=element["id"],
            name=brand,
            lat=lat,
            lng=lng
        ))

init_shops()

@app.get("/stores", response_model=list[Shop])
async def get_stores():
    return MOCK_SHOPS