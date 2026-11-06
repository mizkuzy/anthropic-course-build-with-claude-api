# Prompt engineering techniques

## Урок 16. Being clear and direct

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/being-clear-and-direct

### Главное

Первая строка prompt — самая важная часть запроса. Она задаёт, что Claude
делает дальше. Первая строка должна быть ясной (clear) и прямой (direct).

### Ясно (clear)

- простые слова, которые поймёт любой;
- сказать прямо, что нужно, без вступлений;
- начать с задачи для Claude.

Плохо: «Мне нужно узнать про те штуки на крышах, которые работают от
солнца, вроде солнечные панели называются».

Хорошо: «Write three paragraphs about how solar panels work.»

### Прямо (direct)

- инструкция, а не вопрос;
- начинать с глагола действия: «Write», «Create», «Generate».

Плохо: «Я читала про возобновляемую энергию, геотермальная звучит
интересно. Какие страны её используют?»

Хорошо: «Identify three countries that use geothermal energy. Include
generation stats for each.»

### Пример: план питания

Было (урок 15): «What should this person eat?»

Стало: «Generate a one-day meal plan for an athlete that meets their
dietary restrictions.»

Новая первая строка сразу говорит Claude:
- какое действие сделать — generate;
- что создать — план питания;
- какие ограничения — на один день, для спортсмена, с учётом ограничений в
  питании.

В курсе балл вырос с 2.32 до 3.92 только от изменения первой строки.

### Вывод

Писать prompt как задачу для способного помощника, которому нужно ясное
указание, а не загадку, где он должен угадывать. Начинать с глагола
действия и конкретной задачи.
