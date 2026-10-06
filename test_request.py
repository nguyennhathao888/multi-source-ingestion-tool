import requests

res=requests.get("https://dummyjson.com/products?limit=1")
print(res.status_code)
print(res.json())