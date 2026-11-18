# Tool use with Claude

## Урок 23. Tool schemas

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/tool-schemas

### Главное

После функции пишем для неё JSON schema. По schema Claude понимает, когда
вызывать tool и какие аргументы передать.

JSON Schema — общий стандарт описания и проверки данных, не только для AI.
Его используют для описания параметров функций.

### Из чего состоит описание tool

- `name` — понятное имя tool, например `get_weather`.
- `description` — что делает tool, когда его использовать и что он
  возвращает.
- `input_schema` — JSON schema аргументов функции.

### Как писать description

- 3–4 предложения о том, что делает tool;
- когда Claude должен его использовать;
- какие данные tool возвращает;
- подробное описание каждого аргумента.

### Как сгенерировать schema

Schema не нужно писать вручную, её может написать Claude:

1. Скопировать код функции.
2. Попросить Claude написать JSON schema для tool calling.
3. Приложить документацию Anthropic по tool use:
   https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

Пример prompt: «Write a valid JSON schema spec for the purposes of tool
calling for this function. Follow the best practices listed in the attached
documentation.»

### Schema в коде

Schema кладём рядом с функцией. Имя — `<имя функции>_schema`, чтобы сразу
видеть, к какой функции она относится:

```python
def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

get_current_datetime_schema = {
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "A string specifying the format of the returned datetime. Uses Python's strftime format codes.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
}
```

- `properties` — аргументы функции, у каждого тип и описание.
- `default` — значение по умолчанию.
- `required` пустой: `date_format` необязательный.

### Проверка типов

Schema можно обернуть в `ToolParam` из библиотеки Anthropic:

```python
from anthropic.types import ToolParam

get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    # ... остальная schema
})
```

Работает и без этого, но так редактор проверяет типы и показывает ошибки
до вызова API.
