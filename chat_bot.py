import os
import time
import psycopg2
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_key)

chat_config = types.GenerateContentConfig(
    system_instruction="Ты — опытный наставник по базам данных PostgreSQL и Python. Отвечай кратко, профессионально и всегда приводи примеры кода, если тебя просят что-то объяснить."
)
chat = client.chats.create(model='gemini-3.7-flash', config=chat_config)

def save_message(role, message_text):
    try:
        # Подключаемся к БД (твой системный пользователь Aleksandrvasin имеет к ней доступ по умолчанию)
        conn = psycopg2.connect(dbname="ai_bot_db", user="Aleksandrvasin", host="host.docker.internal")
        cursor = conn.cursor()
        
        # SQL-запрос для вставки данных (используем %s для защиты от SQL-инъекций)
        insert_query = "INSERT INTO chat_messages (role, message_text) VALUES (%s, %s);"
        cursor.execute(insert_query, (role, message_text))
        
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
                print(f"  [Система] Превышен лимит API (429). Попытка {attempt + 1}. Ждем 60 сек...")
                time.sleep(60)
            else:
                return f"Произошла непредвиденная ошибка: {error_msg}"
    return "Не удалось получить ответ. Лимиты исчерпаны или сервер недоступен."

print("Бот запущен! Напиши 'выход' для завершения.\n")

while True:
    message = input("Ты: ")

    if message.lower() == "выход":
        print("Завершение работы. До встречи!")
        break
    
    if not message.strip():
        continue
    
    # 1. Сохраняем вопрос в базу
    save_message("user", message)
    
    answer = get_ai_answer(message)
    print(f"\nAI: {answer}\n")
    
    # 2. Сохраняем ответ в базу
    save_message("ai", answer)
