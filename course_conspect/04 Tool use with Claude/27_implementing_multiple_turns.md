# Tool use with Claude

## Урок 27. Implementing multiple turns

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/implementing-multiple-turns

### Главное

Пишем цикл, который вызывает Claude, пока он запрашивает tools. Если
Claude больше не просит tool, значит, финальный ответ готов.

### Как понять, что Claude просит tool

Смотрим на поле `stop_reason` в ответе. Если Claude решил вызвать tool,
там `"tool_use"`:

```python
if response.stop_reason != "tool_use":
    break  # Claude is done, no more tools needed
```

### Цикл диалога

```python
def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_datetime_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages
```

Цикл идёт, пока Claude не ответит без запроса tools.

### Несколько вызовов tools

В одном ответе Claude может запросить несколько tools. `run_tools`
выбирает из `content` все блоки tool use и обрабатывает каждый:

```python
def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]
    tool_result_blocks = []

    for tool_request in tool_requests:
        # Process each tool request...
```

### Блок tool result

На каждый блок tool use отвечаем блоком tool result. Связь между ними —
через одинаковый id:

```python
tool_result_block = {
    "type": "tool_result",
    "tool_use_id": tool_request.id,
    "content": json.dumps(tool_output),
    "is_error": False
}
```

`json.dumps` превращает результат функции в строку: `content` должен быть
строкой.

### Обработка ошибок

Если tool упал, Claude всё равно должен получить блок tool result —
с текстом ошибки и `is_error: True`:

```python
try:
    tool_output = run_tool(tool_request.name, tool_request.input)
    tool_result_block = {
        "type": "tool_result",
        "tool_use_id": tool_request.id,
        "content": json.dumps(tool_output),
        "is_error": False
    }
except Exception as e:
    tool_result_block = {
        "type": "tool_result",
        "tool_use_id": tool_request.id,
        "content": f"Error: {e}",
        "is_error": True
    }
```

### Выбор функции по имени tool

`run_tool` по имени tool вызывает нужную функцию:

```python
def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "another_tool":
        return another_tool(**tool_input)
    # Add more tools as needed
```

Новый tool добавляем сюда, цикл диалога менять не нужно.

### Весь процесс

1. Отправляем Claude сообщение пользователя и доступные tools.
2. Claude отвечает текстом и/или запросами tools.
3. Выполняем все запрошенные tools и создаём блоки tool result.
4. Отправляем результаты tools в сообщении с ролью `user`.
5. Повторяем, пока Claude не даст финальный ответ.

История сообщений хранит весь контекст, поэтому Claude может опираться на
результаты прошлых tools и дать полный ответ.
