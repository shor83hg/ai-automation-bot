import os
import time
import psycopg2
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat_config = types.GenerateContentConfig(
    system_instruction="Ты — опытный наставник по базам данных PostgreSQL и Python. Отвечай кратко, профессионально и всегда приводи примеры кода, если тебя просят что-то объяснить."
)
chat = client.chats.create(model='gemini-3.7-flash', config=chat_config)

DB_PARAMS = {
    "dbname": "ai_bot_db",
    "user": "ai_user",
    "password": "supersecret",
    "host": "postgres_db"
}

def init_db():
    """Создает таблицу при первом запуске, если её еще нет"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id SERIAL PRIMARY KEY,
                role VARCHAR(50) NOT NULL,
                message_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"  [Ошибка] Не удалось создать таблицу: {e}")

def save_message(role, message_text):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_messages (role, message_text) VALUES (%s, %s);", (role, message_text))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"  [Ошибка БД] Не удалось сохранить сообщение: {e}")

def get_ai_answer(user_message):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = chat.send_message(user_message)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                print(f"  [Система] Сервер занят (503). Попытка {attempt + 1}. Ждем 3 сек...")
                time.sleep(3)
            elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"  [Система] Превышен лимит (429). Попытка {attempt + 1}. Ждем 60 сек...")
                time.sleep(60)
            else:
                return f"Произошла непредвиденная ошибка: {error_msg}"
    return "Не удалось получить ответ."

init_db()
print("Бот запущен! Напиши 'выход' для завершения.\n")

while True:
    message = input("Ты: ")
    if message.lower() == "выход":
        print("Завершение работы. До встречи!")
        break
    if not message.strip():
        continue
    
    save_message("user", message)
    answer = get_ai_answer(message)
    print(f"\nAI: {answer}\n")
    save_message("ai", answer)

