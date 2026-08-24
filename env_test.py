import os
from dotenv import load_dotenv

load_dotenv()

my_name = os.getenv("MY_NAME")
project_name = os.getenv("PROJECT")

print(f"Мое имя: {my_name}")
print(f"Текущий проект: {project_name}")
