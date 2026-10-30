# Prompt evaluation

## Урок 12. Running the eval

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/running-the-eval

### Главное

Собираем основу eval pipeline: каждую задачу из dataset подставляем в
prompt, отправляем Claude и оцениваем ответ. Оценка пока заглушка — grader
будет в следующих уроках.

### Три функции

**`run_prompt`** — подставляет задачу в prompt и возвращает ответ Claude:

```python
def run_prompt(test_case):
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output
```

Prompt пока простой, без инструкций по формату. Поэтому Claude отвечает
многословно — это исправим позже.

**`run_test_case`** — запускает одну задачу и оценивает ответ:

```python
def run_test_case(test_case):
    output = run_prompt(test_case)

    # TODO - Grading
    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
    }
```

`score = 10` — заглушка, чтобы проверить pipeline целиком.

**`run_eval`** — запускает все задачи dataset и собирает результаты:

```python
def run_eval(dataset):
    results = []
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    return results
```

### Запуск

```python
with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
print(json.dumps(results, indent=2))
```

Первый запуск долгий: даже с Haiku около 30 секунд на весь dataset.
Ускорение будет позже.

### Результат

Список объектов, по одному на задачу:
- `output` — полный ответ Claude;
- `test_case` — исходная задача;
- `score` — оценка (пока всегда 10).

Это основа большинства eval pipeline. Сложность дальше — в деталях: лучший
prompt, настоящий grader, ускорение.

### Отличия у нас

У нас `chat` из `helpers.py` принимает ещё `client` и `model`:
`chat(client, model, messages)`.
