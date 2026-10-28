# Accessing Claude with the API

## Урок 7. Response streaming

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/response-streaming

Notebook: [07_streaming.ipynb](../../lesson_scripts/07_streaming.ipynb)

### Главное

Ответ Claude может генерироваться 10–30 секунд. Без streaming пользователь всё это время ждёт и не видит результата. Со streaming текст появляется частями, по мере генерации.

### Как работает

- Без streaming: сервер ждёт полный ответ, потом отправляет его клиенту.
- Со streaming: Claude сразу подтверждает, что начал работу, и присылает серию событий. В каждом — небольшой кусок ответа. Сервер пересылает куски клиенту сразу.

Всё это — один запрос к API.

### События stream

| Событие | Значение |
|---|---|
| MessageStart | начало сообщения |
| ContentBlockStart | начало блока: текст, вызов инструмента и т. д. |
| ContentBlockDelta | кусок сгенерированного текста |
| ContentBlockStop | блок закончен |
| MessageDelta | сообщение закончено |
| MessageStop | конец данных о сообщении |

Текст для пользователя — в событиях ContentBlockDelta.

### Streaming через `stream=True`

```python
messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database")

stream = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    stream=True,
)

for event in stream:
    print(event)
```

Выводит все события подряд.

### Только текст: `messages.stream`

```python
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="")
```

- `text_stream` — отдаёт только куски текста, остальные события пропускает.
- `end=""` — печатать куски подряд, без переноса строки.

### Полное сообщение после streaming

```python
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        pass  # отправить кусок клиенту

    final_message = stream.get_final_message()
```

`get_final_message()` — собирает весь ответ в один объект, например для сохранения в базу.

Итог: пользователь видит текст сразу, а программа получает полный ответ.
