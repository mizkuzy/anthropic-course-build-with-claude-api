# Prompt evaluation

## Урок 10. A typical eval workflow

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/a-typical-eval-workflow

Теория. Код в уроке — только примеры prompt, notebook нет.

### Главное

Evaluation workflow — 5 шагов, чтобы улучшать prompt по оценке, а не наугад. Есть готовые open source и платные инструменты, но можно начать с простого своего варианта.

### Шаг 1. Написать prompt

Первая версия prompt — базовая точка для сравнения:

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

### Шаг 2. Собрать eval dataset

Dataset — примеры входных данных, похожие на реальные запросы в production. Они подставляются в prompt вместо `{question}`.

В примере три вопроса:
- "What's 2+2?"
- "How do I make oatmeal?"
- "How far away is the Moon?"

В реальных проектах записей десятки, сотни или тысячи. Dataset пишут вручную или генерируют через Claude.

### Шаг 3. Прогнать через Claude

Каждый вопрос подставляем в prompt и отправляем Claude. Получаем ответ на каждый вопрос.

### Шаг 4. Прогнать через grader

Grader смотрит на вопрос и ответ Claude и ставит оценку, обычно от 1 до 10 (10 — идеальный ответ).

В примере:
- 2+2 — 10;
- oatmeal — 4;
- Moon — 9.

Средняя оценка: (10 + 4 + 9) / 3 ≈ 7.67. Это объективная метрика prompt.

### Шаг 5. Изменить prompt и повторить

Меняем prompt и прогоняем те же шаги на том же dataset. Например, добавляем инструкцию:

```python
prompt = f"""
Please answer the user's question:

{question}

Answer the question with ample detail
"""
```

Если средняя оценка выросла (например, до 8.7), изменение помогло.

### Что даёт оценка prompt

- сравнивать версии prompt по цифрам;
- брать версию с лучшей оценкой;
- продолжать улучшать prompt.

Так видно, что изменение prompt действительно улучшение, а не просто другой вариант.
