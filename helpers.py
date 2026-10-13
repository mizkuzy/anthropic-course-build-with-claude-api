def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})


def chat(client, model, messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    # Ответ может начинаться с блока thinking, текст ищем по типу блока
    return next(block.text for block in message.content if block.type == "text")
