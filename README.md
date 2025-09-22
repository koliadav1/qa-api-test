# API-сервис для вопросов и ответов

Тестовое задание: реализация REST API для работы с вопросами и ответами.

## Функциональность

### Модели:
- Question (вопрос):
  - id: int
  - text: str
  - created_at: datetime

- Answer (ответ):
  - id: int
  - question_id: int (FK → Question)
  - user_id: str
  - text: str
  - created_at: datetime

### Методы API

#### Вопросы (Questions)
- GET /questions/ — список всех вопросов  
- POST /questions/ — создать новый вопрос  
- GET /questions/{id} — получить вопрос и все его ответы  
- DELETE /questions/{id} — удалить вопрос (вместе с ответами)  

#### Ответы (Answers)
- POST /questions/{id}/answers/ — добавить ответ к вопросу  
- GET /answers/{id} — получить конкретный ответ  
- DELETE /answers/{id} — удалить ответ  

### Бизнес-логика
- Нельзя создать ответ к несуществующему вопросу.  
- Один и тот же пользователь может оставить несколько ответов на один вопрос.  
- При удалении вопроса удаляются все связанные ответы (каскадное удаление).  

---

## Технологии
- Python 3.11+
- FastAPI — фреймворк
- SQLAlchemy — ORM
- Alembic — миграции
- PostgreSQL — база данных
- Docker + docker-compose — контейнеризация
- pytest — тесты
- logging — логирование

---

## Структура проекта
```
app/
  routers/
  database.py
  models.py
  schemas.py
  services.py
  main.py
  dependencies.py
tests/
  conftest.py
  test_api.py
migrations/
alembic.ini
docker-compose.yml
Dockerfile
README.md
requirements.py
```

---

## Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Запустить контейнеры
```bash
docker-compose up --build
```

### 3. Приложение будет доступно по адресу:
- API: http://localhost:8000  
- Swagger-документация: http://localhost:8000/docs  

---

## Миграции

Создание новой миграции:  
```bash
docker-compose exec web alembic revision --autogenerate -m "migration name"
```

Применение миграций:  
```bash
docker-compose exec web alembic upgrade head
```

---

## Тесты

Запуск тестов: 
```bash
docker-compose exec web pytest
```

---

## Пример запросов

Создать вопрос:
```http
POST /questions/
Content-Type: application/json

{
  "text": "Тестовый вопрос?"
}
```
Добавить ответ:
```http
POST /questions/1/answers/
Content-Type: application/json

{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "text": "Тестовый ответ."
}
```