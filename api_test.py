import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos/1")

print(response.status_code)

data = response.json()

print(data)
print(data["title"])
print(data["completed"])
           