import requests

query = """[out:json][timeout:25];(node["shop"="supermarket"](50.0,19.8,50.1,20.1);way["shop"="supermarket"](50.0,19.8,50.1,20.1););out center;"""
response = requests.post(
    "https://overpass-api.de/api/interpreter",
    data={"data": query},
)

print("Status:", response.status_code)
print("Body:", response.text[:500])