# Урок 5. System prompts

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/system-prompts

Notebook: [05_math_tutor.ipynb](../../lesson_scripts/05_math_tutor.ipynb)

## Главное

System prompt — инструкция для Claude, как отвечать: роль, тон, стиль, ограничения. Claude отвечает так, как ответил бы человек в этой роли, и не уходит от задачи.

## Пример: репетитор по математике

Ученик спрашивает: «How do I solve 5x + 2 = 3 for x?»

Нужно:
- сначала давать подсказки, а не готовое решение;
- вести по шагам;
- показывать решение похожих задач.

Не нужно:
- сразу давать ответ;
- советовать калькулятор.

## Как передать system prompt

Обычная строка в параметре `system` функции `create`:

```python
system_prompt = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""

client.messages.create(
    model=model,
    messages=messages,
    max_tokens=1000,
    system=system_prompt,
)
```

Результат:
- без system prompt — Claude сразу пишет полное решение;
- с system prompt — Claude задаёт наводящие вопросы, например, какой первый шаг поможет выделить x.

## `chat` с необязательным system prompt

```python
def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

- API не принимает `system=None`, поэтому `system` добавляется в параметры, только если он задан.
- `**params` — передаёт словарь как именованные аргументы.

Вызов:

```python
answer = chat(messages)                 # без system prompt
answer = chat(messages, system=system)  # с system prompt
```

## Отличия у нас

В `helpers.py` функция `chat` принимает `client` и `model` аргументами и ищет блок с типом `text` (см. урок 4). Вызов: `chat(client, model, messages, system=system)`.
