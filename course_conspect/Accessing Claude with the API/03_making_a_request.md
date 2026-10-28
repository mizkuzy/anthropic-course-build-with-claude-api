# Урок 3. Making a request

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/making-a-request

Notebook: [03_first_request.ipynb](../../lesson_scripts/03_first_request.ipynb)

## 1. Библиотеки

В уроке: `%pip install anthropic python-dotenv` в ячейке notebook.

У нас уже установлены в `.venv` (см. `SETUP.md`), этот шаг пропускаем.

## 2. Ключ в `.env`

Файл `.env` рядом с notebook:

```
ANTHROPIC_API_KEY="ключ"
```

Зачем: ключ не попадает в код и в git. `.env` записан в `.gitignore`.

## 3. Клиент

Модель изменена: в уроке `claude-sonnet-4-5`, но она устарела, и API на неё отвечает ошибкой 404, поэтому используем `claude-sonnet-5-5`.

```python
from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-5-5"
```

- `load_dotenv()` — читает `.env` и делает ключ доступным программе.
- `Anthropic()` — создаёт клиент, ключ берёт сам.
- `model` — имя модели для запросов.

Результат запуска: вывода нет, слева `[1]`.

## 4. Запрос

```python
message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "What is quantum computing? Answer in one sentence"}
    ],
)
```

- `max_tokens` — верхний предел длины ответа, не цель. Модель не старается его достичь.
- `messages` — история диалога. Роли: `user` — текст человека, `assistant` — ответы модели.

## 5. Текст ответа

```python
message.content[0].text
```

Объект ответа содержит много данных. Текст лежит в `content[0].text`.
