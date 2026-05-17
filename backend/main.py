import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Shop(BaseModel):
    id: int
    brand: str
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
            brand=brand,
            lat=lat,
            lng=lng
        ))

init_shops()

@app.get("/stores", response_model=list[Shop])
async def get_stores():
    return MOCK_SHOPS