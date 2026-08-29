import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

print("Список актуальных моделей:")
for model in client.models.list():
    print(model.name)
