# Урок 8. Structured data

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/structured-data

Notebook: [08_structured_data.ipynb](../../lesson_scripts/08_structured_data.ipynb)

**Неактуально для новых моделей.** Приём урока — prefill (начало ответа за Claude в сообщении `assistant`). На Claude Sonnet 5.5 prefill возвращает ошибку 400. Источник: https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide — в списке настроек, которые возвращают 400, есть «assistant prefill».

Теперь формат ответа задают параметром `output_config`: в `output_config.format` передают JSON Schema, и API возвращает JSON по этой схеме. Пример — в нашем notebook [08_structured_data.ipynb](../../lesson_scripts/08_structured_data.ipynb), документация — https://platform.claude.com/docs/en/build-with-claude/structured-outputs.

## Главное

Когда нужны только данные (JSON, код, список), Claude часто добавляет к ним markdown-блок и пояснения. Для приложения это мешает: пользователь не может скопировать ответ целиком.

## Пример задачи

Веб-приложение генерирует правила AWS EventBridge. Пользователь вводит описание и ждёт чистый JSON.

По умолчанию Claude отвечает так: JSON в блоке ```` ```json ````, а после блока — пояснение.

## Решение урока: prefill + stop sequence

```python
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
```

Как работает:
1. Сообщение `user` говорит, что сгенерировать.
2. Сообщение `assistant` с ```` ```json ```` — Claude считает, что уже открыл блок кода.
3. Claude продолжает и пишет только JSON.
4. Когда Claude закрывает блок ```` ``` ````, stop sequence сразу останавливает генерацию.

Результат — JSON без markdown и пояснений.

## Обработка ответа

В начале и в конце ответа бывают лишние переносы строк:

```python
import json

clean_json = json.loads(text.strip())
```

- `strip()` — убирает пробелы и переносы по краям.
- `json.loads()` — превращает строку JSON в объект Python.

## Не только JSON

Приём подходит для кода, списков, CSV и любых данных без комментариев. Нужно понять, во что Claude оборачивает ответ, и использовать это как prefill и stop sequence.

## Для нашей модели: structured outputs

Вместо prefill — параметр `output_config.format` с JSON Schema. API гарантирует, что текст ответа — валидный JSON по этой схеме, без markdown и пояснений.

```python
import json

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": "Generate a very short event bridge rule as json"}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "source": {"type": "array", "items": {"type": "string"}},
                    "detail-type": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["source", "detail-type"],
                "additionalProperties": False,
            },
        }
    },
)

text = next(block.text for block in response.content if block.type == "text")
rule = json.loads(text)
```

- `schema` — какие поля и каких типов должны быть в JSON.
- `required` — обязательные поля.
- `additionalProperties: False` — других полей быть не может.
- Ответ может начинаться с блока `thinking`, поэтому текст ищем по типу блока, как в `chat`.

Источник: справка по Claude API в Claude Code (skill `claude-api`), раздел Structured Outputs. Проверено на API: ответ — `{'source': ['aws.ec2'], 'detail-type': ['EC2 Instance State-change Notification']}`.
