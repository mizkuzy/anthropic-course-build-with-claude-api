# Prompt evaluation

## Урок 11. Generating test datasets

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/generating-test-datasets

**Неактуально для новых моделей.** Dataset в уроке генерируют через prefill и `temperature`. На Claude Sonnet 5.5 оба дают ошибку 400 — см. уроки 6 и 8 и https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide.

Чтобы получить JSON, используем `output_config` (structured outputs), как в уроке 8. Документация — https://platform.claude.com/docs/en/build-with-claude/structured-outputs.

### Главное

Начало своего eval workflow: пишем первую версию prompt и генерируем для неё тестовые данные через Claude.

### Задача

Prompt помогает писать код для задач AWS. Ответ — один из трёх форматов:
- код на Python;
- JSON-конфиг;
- регулярное выражение (regex).

Требование: в ответе только результат, без пояснений, заголовков и текста после него.

Версия 1 prompt:

```python
prompt = f"""
Please provide a solution to the following task:
{task}
"""
```

### Eval dataset

Dataset — список JSON-объектов. В каждом поле `task` — описание задачи. Каждую задачу подставляем в prompt, запускаем и оцениваем результат.

Dataset можно написать вручную или сгенерировать через Claude. Для генерации курс советует быструю модель Haiku: качество тут менее важно.

### Решение урока: генерация через prefill

Функция `generate_dataset` просит Claude сгенерировать 3 задачи. Важные пункты prompt:
- задача решается одной функцией Python, одним JSON-объектом или одним regex;
- кода в решении немного;
- пример формата ответа: `[{"task": "Description of task"}, ...]`.

Чтобы получить чистый JSON, используют приём из урока 8:

```python
messages = []
add_user_message(messages, prompt)
add_assistant_message(messages, "```json")
text = chat(messages, stop_sequences=["```"])
return json.loads(text)
```

`chat` в уроке также принимает `temperature` и `stop_sequences`.

### Для нашей модели: structured outputs

Вместо prefill передаём схему в `output_config.format`. Корень схемы — объект, поэтому список задач лежит в поле `tasks`:

```python
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[{"role": "user", "content": prompt}],
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"task": {"type": "string"}},
                            "required": ["task"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["tasks"],
                "additionalProperties": False,
            },
        }
    },
)

text = next(block.text for block in response.content if block.type == "text")
dataset = json.loads(text)["tasks"]
```

Код ещё не проверен на API.

### Сохранение dataset

Сохраняем в файл, чтобы потом загрузить при evaluation:

```python
with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)
```

`dataset.json` создаётся в папке notebook. `indent=2` — JSON с отступами, его удобно читать.
