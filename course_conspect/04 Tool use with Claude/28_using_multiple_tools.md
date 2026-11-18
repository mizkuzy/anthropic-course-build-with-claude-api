# Tool use with Claude

## Урок 28. Using multiple tools

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/using-multiple-tools

### Главное

Когда основной код для tools готов, новые tools добавлять просто.

### Какие tools добавляем

Для системы напоминаний нужны три tools:

- **Get current date time** — Claude должен знать текущие дату и время.
- **Add duration to date time** — Claude не всегда правильно прибавляет
  время к дате.
- **Set a reminder** — способ поставить напоминание.

Функции `add_duration_to_datetime` и `set_reminder` и их schemas в уроке
даны готовыми.

### Tools в цикле диалога

В уроке список tools записан внутри `run_conversation`, поэтому новые
schemas добавляют в её код:

```python
response = chat(messages, tools=[
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema
])
```

Так Claude узнаёт обо всех трёх tools.

### Выбор функции по имени tool

В `run_tool` добавляем `elif` для каждого нового tool:

```python
def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
```

Проверяем имя tool, вызываем нужную функцию с полученными параметрами,
возвращаем результат.

### Проверка

Запрос, для которого нужно несколько tools: «Set a reminder for my doctors
appointment. Its 177 days after Jan 1st, 2050.»

Claude должен:

1. Вычислить дату через `add_duration_to_datetime`.
2. Поставить напоминание через `set_reminder`.

Claude сначала пишет, что собирается сделать, потом по очереди вызывает
tools. Он получает дату 27 июня 2050 года и ставит напоминание на неё.

### Сообщения в истории

В истории сообщений видно:

1. Сообщение пользователя с запросом.
2. Ответ Claude с текстом и блоками tool use.
3. Сообщения с результатами tools.
4. Следующие ответы Claude.

В одном сообщении Claude может совмещать пояснение текстом и запросы
tools.

### Как добавить новый tool

1. Написать функцию tool.
2. Написать её schema.
3. Добавить schema в список `tools` в `run_conversation`.
4. Добавить вызов функции в `run_tool`.

Существующий код менять не нужно: новый tool работает с тем же циклом
диалога и обработкой tools.

### Что мы поменяли

У нас `run_conversation` получает список tools аргументом, её код менять
не нужно. Все три schemas передаём при вызове:

```python
run_conversation(client, model, messages, tools=[
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
])
```
