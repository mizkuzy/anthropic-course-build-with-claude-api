from anthropic.types import Message


def add_user_message(messages, message):
    # message — текст, список блоков или ответ Claude (Message)
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "user", "content": content})


def add_assistant_message(messages, message):
    # Сохраняем все блоки ответа: текст и tool use
    content = message.content if isinstance(message, Message) else message
    messages.append({"role": "assistant", "content": content})


def chat(client, model, messages, system=None, tools=None, thinking=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    # API не принимает None, поэтому добавляем только заданные параметры
    if system:
        params["system"] = system
    if tools:
        params["tools"] = tools
    if thinking:
        params["thinking"] = thinking

    # Возвращаем весь ответ: в нём могут быть блоки tool use
    return client.messages.create(**params)


def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
