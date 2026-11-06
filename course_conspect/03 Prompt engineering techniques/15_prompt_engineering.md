# Prompt engineering techniques

## Урок 15. Prompt engineering

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/prompt-engineering

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
