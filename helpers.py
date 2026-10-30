def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(client, model, messages, system=None, stream=False):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "stream": stream,
    }
    # API не принимает system=None, поэтому добавляем только если задан
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    # stream=True: возвращаем поток событий, а не текст
    if stream:
        return message

    # Ответ может начинаться с блока thinking, текст ищем по типу блока
    return next(block.text for block in message.content if block.type == "text")


def print_results(results):
    # Печатаем поля отдельно, чтобы переносы строк в ответе были настоящими
    for result in results:
        print("TASK:", result["test_case"]["task"])
        print("SCORE:", result["score"])
        print(result["output"])
        print("-" * 80)
