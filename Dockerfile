# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.12-slim

# Встановимо змінну середовища
ENV APP_HW /hw2

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HW

# Встановимо залежності всередині контейнера
COPY pyproject.toml $APP_HW/pyproject.toml
COPY poetry.lock $APP_HW/poetry.lock

# Встановимо залежності всередині контейнера
RUN pip install poetry
RUN poetry config virtualenvs.create false $$ poetry install --only main

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 5000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "hw8.py"]