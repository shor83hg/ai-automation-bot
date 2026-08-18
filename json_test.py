import json

with open('data.json', 'r') as file:
    data = json.load(file)

print(data)
print(data["name"])
print(data["profession"])
print(data["learning hours"])
print(data["skills"])