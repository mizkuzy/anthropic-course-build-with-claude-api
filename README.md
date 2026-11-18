# Building with the Claude API

Конспекты и код по курсу Anthropic Academy
[Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api).

## Структура

- `course_conspect/` — конспекты уроков на русском, по папкам модулей.
- `lesson_scripts/` — Jupyter notebook уроков и файлы данных к ним.
- `lesson_scripts/reminders/` — проект модуля «Tool use with Claude»:
  Claude ставит напоминания с помощью tools.
- `helpers.py` — общие функции для запросов к Claude.
- `prompt_evaluator.py` — `PromptEvaluator` для модуля «Prompt
  engineering techniques».

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install notebook anthropic python-dotenv
```

API-ключ положить в файл `.env` в корне проекта:

```
ANTHROPIC_API_KEY="ключ"
```

Запустить Jupyter:

```bash
jupyter notebook
```

Подробнее — в [SETUP.md](SETUP.md).
