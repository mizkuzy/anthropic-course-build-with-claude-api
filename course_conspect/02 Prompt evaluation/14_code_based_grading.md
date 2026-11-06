# Prompt evaluation

## Урок 14. Code based grading

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/code-based-grading

Notebook: [14_code_based_grading.ipynb](../../lesson_scripts/14_code_based_grading.ipynb)

**Неактуально для новых моделей.** Чтобы Claude вернул только код, урок
использует prefill ```` ```code ````. На Claude Sonnet 5.5 prefill даёт
ошибку 400 — см. урок 8 и
https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide.

Без prefill формат задаём инструкциями в prompt (раздел «Более точный
prompt»). Другой вариант — structured outputs с полем для кода, как в
уроке 11: https://platform.claude.com/docs/en/build-with-claude/structured-outputs.

В нашем notebook код приходит через structured outputs в поле `code`.
Проверено на API (Haiku 5.5): только с инструкциями в prompt Claude
оборачивал код в блок ```` ``` ```` и синтаксис Python и JSON получал 0,
средний балл 5.83. Со structured outputs синтаксис везде 10, средний
балл 9.17.

### Главное

Grader на коде проверяет, что сгенерированный код синтаксически верный и в
ответе только код. Его оценку объединяем с оценкой grader на модели.

### Кто какой критерий проверяет

- **Формат** — только Python, JSON или regex, без пояснений → код;
- **Синтаксис** — код парсится как нужный язык → код;
- **Выполнение задачи** — ответ решает задачу правильно → модель.

Вместе два grader дают более полную оценку.

### Функции проверки синтаксиса

Каждая пробует распарсить текст. Получилось — 10, ошибка — 0:

```python
def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0
```

- `json.loads` — парсит JSON;
- `ast.parse` — парсит код Python, но не запускает его;
- `re.compile` — компилирует regex.

Если в ответе есть пояснения или markdown-блок, парсинг не пройдёт и
оценка будет 0. Так проверяется и формат.

### Формат в dataset

Чтобы выбрать нужную функцию, в каждой задаче dataset указываем формат:

```json
{
  "task": "Create a Python function to validate an AWS IAM username",
  "format": "python"
}
```

Для этого добавляем поле `format` в пример ответа в prompt генерации
dataset (урок 11).

### Более точный prompt

Добавляем в prompt инструкции о формате:

```
* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation
```

### Объединение оценок

Простой способ — среднее двух оценок:

```python
model_grade = grade_by_model(test_case, output)
model_score = model_grade["score"]
syntax_score = grade_syntax(output, test_case)

score = (model_score + syntax_score) / 2
```

Так качество ответа и техническая правильность весят одинаково. Веса можно
менять под задачу.

### Базовая оценка

Первый запуск с grader на коде даёт базовую оценку. Сама по себе она не
хорошая и не плохая. Важно, растёт ли она, когда меняем prompt. Так
прогресс prompt engineering измеряется числом, а не на глаз.
