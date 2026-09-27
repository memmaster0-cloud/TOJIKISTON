# ToDo API

![CI/CD](https://github.com/USERNAME/todo-api/actions/workflows/ci.yml/badge.svg)

Простой REST API для управления списком задач (ToDo), написанный на
Flask. Хранит задачи в памяти процесса.

Итоговый проект по дисциплине «Технологии разработки программного
обеспечения»: приложение + Git/GitHub + линтеры + тесты + Docker + CI/CD.

## Функциональность

| Метод  | Путь           | Описание                          |
|--------|----------------|------------------------------------|
| GET    | `/health`      | Проверка работоспособности         |
| GET    | `/todos`       | Список всех задач                  |
| POST   | `/todos`       | Создать задачу (`{"title": str}`)  |
| GET    | `/todos/<id>`  | Получить задачу по id              |
| PUT    | `/todos/<id>`  | Обновить задачу (`title`, `done`)  |
| DELETE | `/todos/<id>`  | Удалить задачу                     |

## Запуск через Docker

```bash
docker build -t todo-api .
docker run -p 5000:5000 todo-api
```

Или готовый образ с Docker Hub (после публикации через CI):

```bash
docker run -p 5000:5000 memmaster0-cloud/todo-api:latest
```

Приложение будет доступно на `http://localhost:5000`.

## Запуск локально (без Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m flask --app app:create_app run
```

## Примеры использования

```bash
curl -X POST http://localhost:5000/todos -H "Content-Type: application/json" \
  -d '{"title": "Купить молоко"}'

curl http://localhost:5000/todos
```

## Разработка

Установка pre-commit хуков:

```bash
pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

Запуск тестов с покрытием:

```bash
pytest --cov=app --cov-report=term tests/
```

## Docker Hub

Образ публикуется автоматически при пуше в `main`:
`https://hub.docker.com/r/memmaster0-cloud/todo-api`

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) при push/PR в `main`:
устанавливает зависимости → линтинг (flake8) → проверка форматирования
(black, isort) → тесты с покрытием (pytest-cov) → сборка и публикация
Docker-образа на Docker Hub.
