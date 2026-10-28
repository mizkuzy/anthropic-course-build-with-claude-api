# Accessing Claude with the API

## Урок 6. Temperature

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/temperature

**Неактуально для новых моделей.** На Claude Sonnet 5.5 значение temperature не по умолчанию возвращает ошибку 400. Менять temperature можно на Claude Sonnet 4.6, более ранних моделях и Claude Haiku 4.5. Источник: https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide, раздел «Sampling parameters return an error».

### Главное

Temperature — число от 0 до 1. Задаёт, насколько ответ предсказуемый или разнообразный.

### Как Claude выбирает слова

1. Токенизация — ввод делится на токены.
2. Предсказание — модель считает вероятность каждого возможного следующего токена.
3. Выбор — модель выбирает токен по этим вероятностям и повторяет шаги.

Пример: после «What do you think» — «about» 30 %, «would» 20 %, «of» 10 % и т. д.

### Что делает temperature

- Около 0 — модель почти всегда берёт самый вероятный токен. Ответы одинаковые.
- Около 1 — вероятности распределяются ровнее. Ответы разнообразнее.

### Какую выбрать

| Temperature | Задачи |
|---|---|
| 0.0–0.3 | факты, код, извлечение данных, модерация |
| 0.4–0.7 | пересказ, учебные материалы, решение задач, творческий текст с ограничениями |
| 0.8–1.0 | брейншторм, творческий текст, маркетинг, шутки |

### `chat` с temperature

```python
def chat(messages, system=None, temperature=1.0):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }
    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text
```

Изменения: аргумент `temperature=1.0` и ключ `"temperature"` в `params`.

### Проверка

Попросить идею фильма с разной temperature:

```python
answer = chat(messages, temperature=0.0)  # предсказуемо
answer = chat(messages, temperature=1.0)  # разнообразно
```

При 0.0 ответы повторяются, при 1.0 меняются темы, герои и сюжет.

Temperature не гарантирует разные ответы, а только меняет вероятность. При высокой temperature ответы тоже иногда похожи.

### Отличия у нас

В `helpers.py` вызов: `chat(client, model, messages, system=system, temperature=0.0)`.
