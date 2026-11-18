# Tool use with Claude

## Урок 24. Handling message blocks

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/handling-message-blocks

### Главное

С tools ответ Claude состоит не из одного текстового блока, а из
нескольких: текст и запрос на вызов tool.

### Запрос с tools

Список schemas передаём в параметре `tools`:

```python
messages = []
messages.append({
    "role": "user",
    "content": "What is the exact time, formatted as HH:MM:SS?"
})

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema],
)
```

### Ответ из нескольких блоков

Если Claude решает вызвать tool, в `content` ответа несколько блоков:

- **Text** — текст для человека, например «I can help you find out the
  current time. Let me find that information for you».
- **ToolUse** — указание нашему коду, какой tool вызвать и с какими
  параметрами.

В блоке ToolUse:

- `id` — идентификатор вызова;
- `name` — имя функции, например `get_current_datetime`;
- `input` — параметры в виде словаря;
- `type` — `"tool_use"`.

### История сообщений

Claude не хранит историю, мы передаём её сами. Ответ сохраняем целиком,
со всеми блоками:

```python
messages.append({
    "role": "assistant",
    "content": response.content
})
```

Так в истории остаются и текст, и блок tool use. Они нужны Claude
в следующих запросах.

### Весь процесс

1. Отправляем сообщение пользователя и schema tool.
2. Получаем ответ: текст и блок tool use.
3. Берём из блока имя и параметры, вызываем функцию.
4. Отправляем результат tool и всю историю сообщений.
5. Получаем финальный ответ Claude.

### Helper-функции

`add_user_message()` и `add_assistant_message()` нужно доработать: сейчас
они работают только с одним текстовым блоком, а теперь `content` может
содержать несколько блоков.
