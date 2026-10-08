# Окружение для курса «Building with the Claude API»

## Где всё лежит

```
~/Documents/learn_programming/anthropic-course-build-with-claude-api/
└── .venv/    ← виртуальное окружение
```

## Почему venv

Python на этом Mac установлен через Homebrew и не даёт ставить библиотеки глобально (ошибка `externally-managed-environment`).

venv — отдельная папка со своим Python и библиотеками только для курса:

- не трогает системный Python, AWS-конфиги (`~/.aws`), Claude Code;
- работает только в окне терминала, где его включили;
- удалить всё = удалить папку курса.

Важно: venv хранит свой полный путь. Папку с `.venv` нельзя перемещать — проще удалить `.venv` и создать заново.

## Что установлено

```
pip install notebook anthropic python-dotenv
```

- `notebook` — Jupyter, где пишут и запускают код по ячейкам;
- `anthropic` — библиотека для запросов к Claude;
- `python-dotenv` — читает API-ключ из файла `.env`.

## Каждый раз, чтобы начать работу

```
cd ~/Documents/learn_programming/anthropic-course-build-with-claude-api
source .venv/bin/activate
jupyter notebook
```

В начале строки терминала должно быть `(.venv)`.

Если браузер не открылся сам — скопировать из лога в терминале ссылку `http://localhost:8888/tree?token=...` и открыть её в браузере. Токен каждый раз новый.

Не закрывать окно терминала, пока работает Jupyter.

Закончить: остановить Jupyter (`Ctrl + C` в терминале), затем `deactivate`.

## Где писать код

Код курса пишется в файле Jupyter notebook (`.ipynb`).

- Создать: в Jupyter New → Notebook → kernel Python 3.
- Запустить ячейку: `Shift + Enter`.

## API-ключ

- Хранить только в файле `.env` в папке курса:
  ```
  ANTHROPIC_API_KEY="ключ"
  ```
- Добавить `.env` в `.gitignore`.
- НЕ добавлять ключ в `~/.zshrc`: иначе Claude Code начнёт тратить деньги API вместо подписки.

## Создать окружение заново

```
cd ~/Documents/learn_programming/anthropic-course-build-with-claude-api
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install notebook anthropic python-dotenv
```
