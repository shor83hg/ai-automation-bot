def get_answer(message):
    if message == "привет":
        return "Привет, Александр!"
    elif message == "python":
        return "Python - отличный выбор для AI Automation."
    else:
        return "Пока я не знаю, как ответить на это."

while True:
    message = input("Ты: ").lower()
 
    if message == "выход":
        break
    else:
        answer = get_answer(message)
        print(answer)