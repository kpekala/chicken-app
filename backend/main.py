import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# [out:json][timeout:60];(
#   node["industrial"="slaughterhouse"]({{bbox}});
#   way["industrial"="slaughterhouse"]({{bbox}});
#   node["building"="fur_farm"]({{bbox}});
#   way["building"="fur_farm"]({{bbox}});
#   node["animal"="fur"]({{bbox}});
#   relation["farmyard"="poultry"]({{bbox}});
#   way["farmyard"="poultry"]({{bbox}});
#   node["farmyard"="poultry"]({{bbox}});
#   way["animal"="fur"]({{bbox}}););out center;

#uvicorn main:app --reload
#venv\Scripts\activate

class Polygon(BaseModel):
    id: int
    name: str
    type: str  # forest, nature_reserve, protected_area
    outer: list[list[tuple[float, float]]]
    inner: list[list[tuple[float, float]]] 

class Shop(BaseModel):
    id: int
    name: str
    lat: float
    lng: float

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_POLYGONS: list[Polygon] = []

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

def init_polygons():
    with open("polygons.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for element in data["elements"]:
        if element["type"] != "relation":
            continue

        tags = element.get("tags", {})
        name = tags.get("name") or tags.get("ref")

        if not name:
            continue

        # determine type
        if tags.get("boundary") == "protected_area":
            area_type = "protected_area"
        elif tags.get("leisure") == "nature_reserve":
            area_type = "nature_reserve"
        elif tags.get("landuse") == "forest":
            area_type = "forest"
        else:
            continue

        # extract polygon rings from members
        outer_rings = []
        inner_rings = []

        for member in element.get("members", []):
            if member.get("type") != "way":
                continue
            ring = [
                (node["lat"], node["lon"])
                for node in member.get("geometry", [])
            ]
            if not ring:
                continue
            
            role = member.get("role", "outer")
            if role == "inner":
                inner_rings.append(ring)
            else:
                outer_rings.append(ring)

        if not outer_rings:
            continue

        MOCK_POLYGONS.append(Polygon(
            id=element["id"],
            name=name,
            type=area_type,
            outer=outer_rings,
            inner=inner_rings
        ))

init_polygons()

init_shops()

@app.get("/stores", response_model=list[Shop])
async def get_stores():
    return MOCK_SHOPS

@app.get("/polygons", response_model=list[Polygon])
async def get_polygons():
    return MOCK_POLYGONS