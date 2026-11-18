# Tool use with Claude

## Урок 26. Multi-turn conversations with tools

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/multi-turn-conversations-with-tools

### Главное

Чтобы ответить на один вопрос, Claude может вызвать несколько tools подряд.
Например, на вопрос «What day is 103 days from today?» он сначала узнаёт
текущую дату, потом прибавляет к ней 103 дня. Приложение должно
обрабатывать такие цепочки вызовов само.

### Как это происходит

1. Пользователь спрашивает: «What day is 103 days from today?»
2. Claude отвечает блоком tool use с запросом `get_current_datetime`.
3. Сервер вызывает функцию и отправляет результат.
4. Claude понимает, что данных мало, и запрашивает
   `add_duration_to_datetime`.
5. Сервер вызывает эту функцию и отправляет результат.
6. Теперь у Claude достаточно данных, и он даёт финальный ответ.

### Цикл диалога

Цикл продолжается, пока Claude запрашивает tools:

```python
def run_conversation(messages):
    while True:
        response = chat(messages)

        add_assistant_message(messages, response)

        # Pseudo code
        if response isn't asking for a tool:
            break

        tool_result_blocks = run_tools(response)
        add_user_message(messages, tool_result_blocks)

    return messages
```

Это псевдокод: проверку и `run_tools` напишем в следующем уроке.

### Доработка helper-функций

Перед циклом дорабатываем helper-функции, чтобы они работали
с сообщениями из нескольких блоков.

**`add_user_message` и `add_assistant_message`** принимают строку, список
блоков или весь ответ Claude (`Message`):

```python
from anthropic.types import Message

def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)
```

`isinstance(message, Message)` проверяет, что передан ответ Claude. Тогда
берём его `content` со всеми блоками. `add_assistant_message` такая же,
с ролью `assistant`.

**`chat`** принимает список tools и возвращает весь ответ, а не только
текст:

```python
def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message
```

**`text_from_message`** — новая функция. Собирает текст из всех текстовых
блоков ответа, например чтобы показать пользователю финальный ответ:

```python
def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )
```

### Что это даёт

- helper-функции работают с разными форматами сообщений;
- `chat` передаёт schemas tools в API;
- `chat` возвращает весь ответ, все блоки сохраняются;
- `text_from_message` достаёт текст из ответа.

Теперь можно написать цикл, который сам обрабатывает несколько вызовов
tools.

### Код проекта

Helper-функции проекта напоминаний лежат в
[chat.py](../../lesson_scripts/reminders/chat.py).

### Что мы поменяли

В `chat`:

- нет `temperature`: на новых моделях она даёт ошибку 400;
- нет `stop_sequences`: в проекте они не нужны;
- `client` и `model` передаются аргументами, как в корневом `helpers.py`;
- есть параметр `thinking`, как в корневом `helpers.py`.
