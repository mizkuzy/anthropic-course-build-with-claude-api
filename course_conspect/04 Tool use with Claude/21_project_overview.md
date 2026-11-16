# Tool use with Claude

## Урок 21. Project overview

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/project-overview

### Главное

Проект модуля — научить Claude ставить напоминания на будущие даты.
Пишем Claude «Set a reminder for my doctor's appointment. It's a week from
Thursday», он отвечает «OK, I will remind you».

### Почему это сложно

- Claude может знать текущую дату, но не точное время.
- Claude не всегда правильно прибавляет время к дате, особенно на много
  дней вперёд.
- У Claude нет способа поставить напоминание.

### Нужные tools

Для каждой проблемы — свой tool:

1. **Get current date time** — текущие дата и время.
2. **Add duration to date time** — прибавить к дате срок.
3. **Set a reminder** — поставить напоминание в системе.

Делаем tools по одному, начинаем с самого простого. В конце Claude сам
комбинирует их: по запросу «remind me in a week» вычисляет точное время и
ставит напоминание.

Принцип: если у модели есть ограничение, расширяем её возможности tools,
а не обходим ограничение в prompt.
