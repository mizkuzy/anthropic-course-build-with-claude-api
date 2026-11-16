# Prompt engineering techniques

## Урок 19. Providing examples

Ссылка: https://academy.claude.com/courses/building-with-the-claude-api/providing-examples

### Главное

Примеры в prompt — одна из самых сильных техник. Даём Claude пары «вход →
идеальный ответ», и он отвечает по их образцу. Называется one-shot или
multi-shot prompting.

### Пример: анализ тональности

Задача: определить, позитивный твит или негативный.

Сложность — сарказм. «Yeah, sure, that was the best movie I've seen since
'Plan 9 from Outer Space'» выглядит позитивным, но это сарказм: «Plan 9» —
один из самых плохих фильмов в истории. Твит негативный.

Решение — добавить в prompt примеры: обычный позитивный, саркастичный и
объяснение, что к сарказму нужно относиться внимательно. Каждый пример
обёрнут в XML-теги `<sample_input>` и `<ideal_output>`, чтобы Claude видел,
где вход, а где ответ:

```
<sample_input>
Great game tonight!
</sample_input>
<ideal_output>
Positive
</ideal_output>

<sample_input>
Oh yeah, I really needed a flight delay tonight! Excellent!
</sample_input>
<ideal_output>
Negative
</ideal_output>
```

### Когда использовать

- крайние и сложные случаи;
- сложный формат ответа, например определённая структура JSON;
- нужен конкретный стиль или тон;
- показать, как обрабатывать неоднозначный вход.

### One-shot и multi-shot

- **One-shot** — один пример, чтобы задать образец.
- **Multi-shot** — несколько примеров для разных случаев. Нужен, когда
  крайних случаев много или правильные ответы бывают разного вида.

### Где взять хорошие примеры

Из eval: берём ответы с баллом 10 (или самым высоким из полученных) и
вставляем эти пары «вход → ответ» в prompt как примеры. Так Claude видит,
как выглядит идеальный ответ именно для этой задачи.

### Объяснять, почему пример хороший

Мало дать пару «вход → ответ», нужно объяснить, чем ответ хорош:

```
<ideal_output>
[пример ответа]
</ideal_output>

This example is well-structured, provides detailed information
on food choices and quantities, and aligns with the athlete's
goals and restrictions.
```

Так Claude понимает не только формат, но и почему ответ хороший.

### Правила

- оборачивать примеры в XML-теги;
- прямо писать, что это: «Here is an example input with an ideal
  response»;
- давать примеры на самые частые ошибки;
- объяснять, почему ответ в примере идеальный;
- примеры должны относиться к этой задаче.

Примеры показывают, а не описывают. Вместо того чтобы объяснять словами,
какой нужен ответ, мы его показываем. Так Claude понимает тонкие
требования, которые сложно описать инструкциями.
