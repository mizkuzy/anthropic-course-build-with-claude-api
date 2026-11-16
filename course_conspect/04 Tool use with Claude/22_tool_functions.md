# Tool use with Claude

## Урок 22. Tool functions

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/tool-functions

### Главное

Tool function — обычная Python-функция. Она выполняется, когда Claude
решает, что ему нужны дополнительные данные. Например, на вопрос «What time
is it?» Claude вызывает tool даты и времени.

### Правила

- **Понятные имена** функции и параметров — по ним видно, что они делают.
- **Проверять входные данные**: если параметр пустой или неверный —
  выбрасывать ошибку.
- **Понятные сообщения об ошибках**: Claude видит текст ошибки и может
  вызвать функцию ещё раз с исправленными параметрами. Например, после
  ошибки «Location cannot be empty» он повторит вызов с городом.

### Первый tool: текущие дата и время

Функция принимает формат даты, чтобы Claude мог запросить время в нужном
виде:

```python
from datetime import datetime

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)
```

- `datetime.now()` — текущие дата и время.
- `strftime(date_format)` — переводит их в строку по формату.
- Формат по умолчанию — «год-месяц-день часы:минуты:секунды».
- Проверка не даёт передать пустой формат.

Вызовы:

```python
get_current_datetime()         # "2024-01-15 14:30:25"
get_current_datetime("%H:%M")  # "14:30"
```

### Дальше

Функция — только первый шаг. Дальше пишем JSON schema, которая описывает
функцию для Claude, и подключаем её к чату.

### Что мы поменяли

Для проекта напоминаний создали папку `lesson_scripts/reminders/`.
Функцию `get_current_datetime` положили в
[tools.py](../../lesson_scripts/reminders/tools.py), чтобы переиспользовать
в следующих уроках.
