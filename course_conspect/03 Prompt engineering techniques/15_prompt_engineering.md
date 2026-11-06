# Prompt engineering techniques

## Урок 15. Prompt engineering

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/prompt-engineering

Notebook: [15_prompt_engineering.ipynb](../../lesson_scripts/15_prompt_engineering.ipynb)

### Главное

Prompt engineering — улучшение уже написанного prompt, чтобы ответы были
стабильнее и качественнее. Улучшаем по шагам и после каждого шага
проверяем оценкой из eval pipeline.

### Цикл улучшения

1. Поставить цель — что prompt должен делать.
2. Написать первую простую версию prompt.
3. Оценить prompt по критериям.
4. Применить технику prompt engineering.
5. Оценить снова — проверить, что изменение улучшило результат.

Шаги 4 и 5 повторяем, пока результат не устроит. Каждая итерация должна
поднимать оценку.

### Пример модуля

Prompt генерирует план питания на один день для спортсмена. Входные
данные: рост, вес, цель и ограничения в питании.

### Eval pipeline: класс PromptEvaluator

В модуле используется класс `PromptEvaluator`. Он генерирует dataset и
оценивает ответы через модель — то, что мы писали сами в уроках 11–14.

```python
evaluator = PromptEvaluator(max_concurrent_tasks=5)
```

`max_concurrent_tasks` — сколько запросов к API идёт одновременно. Курс
советует начать с 3, чтобы не получить ошибку rate limit (превышен лимит
запросов). Если лимиты API позволяют, число можно увеличить.

### Генерация dataset

Описываем задачу и входные данные prompt:

```python
dataset = evaluator.generate_dataset(
    task_description="Write a compact, concise 1 day meal plan "
    "for a single athlete",
    prompt_inputs_spec={
        "height": "Athlete's height in cm",
        "weight": "Athlete's weight in kg",
        "goal": "Goal of the athlete",
        "restrictions": "Dietary restrictions of the athlete",
    },
    output_file="dataset.json",
    num_cases=3,
)
```

- `prompt_inputs_spec` — какие входные данные нужны prompt и что они
  значат;
- `num_cases` — сколько задач сгенерировать.

Пока улучшаем prompt, задач мало (2–3), чтобы каждая итерация шла
быстро. Для финальной проверки число увеличиваем.

### Первая версия prompt

Специально простой prompt — базовая точка для сравнения:

```python
def run_prompt(prompt_inputs):
    prompt = f"""
What should this person eat?

- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary restrictions: {prompt_inputs["restrictions"]}
"""
    messages = []
    add_user_message(messages, prompt)
    return chat(messages)
```

### Дополнительные критерии оценки

В `run_evaluation` можно передать критерии, которые grader на модели
учитывает при оценке:

```python
results = evaluator.run_evaluation(
    run_prompt_function=run_prompt,
    dataset_file="dataset.json",
    extra_criteria="""
The output should include:
- Daily caloric total
- Macronutrient breakdown
- Meals with exact foods, portions, and timing
""",
)
```

Так prompt оценивается по требованиям именно этой задачи: калории за
день, БЖУ (белки, жиры, углеводы), блюда с продуктами, порциями и
временем.

### Результаты

После запуска получаем средний балл и HTML-отчёт. В отчёте для каждой
задачи — балл и объяснение grader. По отчёту видно, где prompt плохой и
что улучшать.

Для первой версии низкий балл — нормально: например, 2.3 из 10.

### Дальше

В следующих уроках применяем техники prompt engineering. Правило: одно
изменение за раз, потом оценка. Так видно, какая техника что даёт.

### Что мы поменяли

**`PromptEvaluator`.** Кода класса в уроке нет. Курс ссылается на файл
`001_prompting.ipynb`, но в Academy его нет. Мы взяли код из репозитория
студента
([jaygaha/Building-with-the-Claude-API](https://github.com/jaygaha/Building-with-the-Claude-API))
и переписали в [prompt_evaluator.py](../../prompt_evaluator.py):
- structured outputs вместо prefill и `temperature` (на новых моделях они
  дают ошибку 400);
- исправили ошибку: описание входных данных не попадало в prompt генерации
  сценариев;
- ответы Claude в HTML-отчёте экранируются, иначе символ `<` ломает
  таблицу.

**Thinking выключен.** Haiku 5.5 по умолчанию сначала думает (блок
`thinking`), и на план питания не хватало `max_tokens`: ответ обрезался
или текста не было совсем. Решение:
- `max_tokens` в `chat` поднят до 4000;
- в `chat` добавлен параметр `thinking`, в notebook передаём
  `{"type": "disabled"}`.

**Три варианта prompt** на одном dataset из 3 задач:

| Вариант | Средний балл | Средняя длина ответа |
|---|---|---|
| простой prompt | 3.0 | ~3200 символов |
| + system prompt для коротких ответов | 2.7 | ~1600 символов |
| + требования к ответу прямо в prompt | 6.3 | ~1800 символов |

Вывод:
- system prompt про стиль сокращает ответ, но балл не поднимает: из
  ответа пропадают калории, БЖУ и порции;
- балл вырос, когда требования (`extra_criteria`) добавили в сам prompt.
  Раньше их видел только grader, а Claude, который писал ответ, не знал,
  что от него ждут.
