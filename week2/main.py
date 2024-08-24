import requests

requests.get

url = "https://dummyjson.com/product"

response = requests.get(
    url,
    params={
        "limit": 10,
        "skip": 5,
        "select": "id,title,price"
    }
    )
print(response.text)
result = response.json()
print(type(result))
result = response.content
print(type(result))
result = response.text
print(type(result))
print(response.json)
limit = response.headers['x-ratelimit-limit']
remaining = response.headers['x-ratelimit-remaining']

response.headers['X-Ratelimt']