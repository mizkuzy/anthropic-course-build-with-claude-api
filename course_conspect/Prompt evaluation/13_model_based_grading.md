# Prompt evaluation

## Урок 13. Model based grading

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/model-based-grading

Notebook: [13_model_based_grading.ipynb](../../lesson_scripts/13_model_based_grading.ipynb)

**Неактуально для новых моделей.** Grader в уроке получает JSON через
prefill. На Claude Sonnet 5.5 prefill даёт ошибку 400 — см. урок 8 и
https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide.

Вместо prefill используем `output_config` (structured outputs), как в
уроках 8 и 11. Документация —
https://platform.claude.com/docs/en/build-with-claude/structured-outputs.

### Главное

Grader получает ответ модели и возвращает измеримую оценку, обычно от 1
до 10. Перед тем как писать grader, нужно определить критерии оценки.

### Три вида grader

| | Код | Модель | Человек |
|---|---|---|---|
| Краткое описание | проверка своей логикой в коде; можно проверить что угодно, что пишется кодом | ответ отправляем ещё одним запросом к API на оценку; очень гибкий способ | человек читает ответы и ставит оценку; самый гибкий способ, но долгий и утомительный |
| Что проверяет | • длину ответа<br>• есть или нет определённых слов<br>• синтаксис JSON, Python или regex<br>• читаемость (readability score) | • качество ответа<br>• насколько точно выполнены инструкции<br>• полноту<br>• полезность<br>• безопасность | • общее качество ответа<br>• насколько ответ всесторонний<br>• глубину<br>• краткость<br>• соответствие вопросу (relevance) |

Grader на коде должен вернуть число, обычно от 1 до 10.

### Критерии для нашего prompt

Prompt генерирует код для AWS (уроки 11–12). Критерии:
- **Формат** — только Python, JSON или regex, без пояснений;
- **Синтаксис** — код синтаксически верный;
- **Выполнение задачи** — ответ решает задачу пользователя правильным
  кодом.

Формат и синтаксис проверяет код. Выполнение задачи — модель, потому что
это сложно описать правилами.

### Решение урока: grader на модели через prefill

```python
def grade_by_model(test_case, output):
    eval_prompt = """
You are an expert code reviewer. Evaluate this AI-generated solution.

Task: {task}
Solution: {solution}

Provide your evaluation as a structured JSON object with:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your assessment
- "score": A number between 1-10
"""
    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)
```

Ошибка в коде курса: `eval_prompt` не f-строка, поэтому `{task}` и
`{solution}` не заменяются на задачу и ответ. Нужно `f"""..."""` и
`{test_case["task"]}`, `{output}`.

 **ВАЖНО**: просить у модели не только оценку, но и сильные стороны,
слабые стороны и объяснение. Без них модель часто ставит средние оценки
около 6.

### Для нашей модели: structured outputs

Схема с полями `strengths`, `weaknesses`, `reasoning`, `score`:

```python
schema = {
    "type": "object",
    "properties": {
        "strengths": {"type": "array", "items": {"type": "string"}},
        "weaknesses": {"type": "array", "items": {"type": "string"}},
        "reasoning": {"type": "string"},
        "score": {"type": "integer"},
    },
    "required": ["strengths", "weaknesses", "reasoning", "score"],
    "additionalProperties": False,
}
```

Схему передаём в `output_config={"format": {"type": "json_schema",
"schema": schema}}`, как в уроке 11. Диапазон 1–10 указываем в тексте
prompt.

Проверено на API (Haiku 5.5): оценки 8, 9 и 8, средняя 8.33.

### Grader в pipeline

`run_test_case` теперь вызывает grader и сохраняет оценку и объяснение:

```python
def run_test_case(test_case):
    output = run_prompt(test_case)

    model_grade = grade_by_model(test_case, output)
    score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning,
    }
```

`run_eval` в конце считает среднюю оценку:

```python
from statistics import mean

average_score = mean([result["score"] for result in results])
print(f"Average score: {average_score}")
```

Средняя оценка — метрика, которую сравниваем между версиями prompt.
Grader на модели иногда даёт разные оценки на одном ответе, но для
сравнения версий prompt его хватает.
