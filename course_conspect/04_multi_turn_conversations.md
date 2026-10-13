# Урок 4. Multi-Turn conversations

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/multi-turn-conversations

Notebook: `multi_turn_chat.ipynb`. Функции урока лежат в `helpers.py`. Клиент создаётся в notebook и передаётся в `chat` аргументом: `chat(client, model, messages)`.

## Главное

API не хранит историю диалога. Каждый запрос независим.

Пример: спросить «What is quantum computing?», затем «Write another sentence». Во втором запросе Claude не знает, о чём речь, и пишет предложение на случайную тему.

## Как сделать диалог

1. Хранить список всех сообщений в своём коде.
2. В каждом запросе отправлять весь список.

Порядок:

1. Отправить первое сообщение `user`.
2. Ответ Claude добавить в список как `assistant`.
3. Добавить следующий вопрос как `user`.
4. Отправить весь список.

## Вспомогательные функции

```python
def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text
```

- `add_user_message` — добавляет в список сообщение человека.
- `add_assistant_message` — добавляет в список ответ Claude.
- `chat` — отправляет весь список и возвращает текст ответа.

## Использование

```python
messages = []

add_user_message(messages, "Define quantum computing in one sentence")
answer = chat(messages)
add_assistant_message(messages, answer)

add_user_message(messages, "Write another sentence")
final_answer = chat(messages)
```

Во втором запросе Claude получает весь диалог и понимает, что нужно продолжить тему quantum computing.

Эти функции используются в следующих уроках.
