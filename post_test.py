import requests

data = {
    "title": "Learning AI Automation",
    "completed": False,
    "userId": 1
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/todos",
    json=data
)

print(response.status_code)
print(response.json())
