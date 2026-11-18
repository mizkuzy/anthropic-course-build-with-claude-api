# Tool use with Claude

## Урок 25. Sending tool results

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/sending-tool-results

### Главное

Когда Claude запросил tool, мы выполняем функцию и отправляем ему
результат. Этим заканчивается процесс tool use.

### Вызов функции

Параметры, которые Claude передаёт в tool, лежат в `input` блока tool use:

```python
response.content[1].input
```

Это словарь. Функция ждёт именованные аргументы, поэтому распаковываем
словарь через `**`:

```python
get_current_datetime(**response.content[1].input)
```

### Блок tool result

Результат функции отправляем Claude в блоке tool result. Этот блок лежит
в сообщении с ролью `user`.

Свойства блока:

- `tool_use_id` — должен совпадать с `id` блока tool use, на который это
  ответ;
- `content` — результат функции в виде строки;
- `is_error` — `True`, если при выполнении была ошибка.

### Несколько вызовов tools

Claude может запросить несколько tools в одном ответе. Например, на вопрос
«What's 10 + 10 and what's 30 + 30?» он может вернуть два блока tool use.

У каждого вызова свой `id`. Результаты отправляем с этими `id`, чтобы
Claude понял, какой результат к какому запросу относится, даже если они
пришли в другом порядке.

### Сообщение с результатом tool

Для следующего запроса добавляем в историю сообщение с результатом tool:

```python
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": response.content[1].id,
        "content": "15:04:22",
        "is_error": False
    }]
})
```

Теперь в истории три сообщения:

1. Исходное сообщение пользователя.
2. Ответ Claude с блоком tool use.
3. Сообщение пользователя с блоком tool result.

### Финальный запрос

Schema tool передаём и в этом запросе, даже если не ждём нового вызова
tool. Без schema Claude не поймёт ссылки на tool в истории сообщений.

```python
client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema]
)
```

Claude отвечает пользователю обычным текстом с учётом результата tool.
