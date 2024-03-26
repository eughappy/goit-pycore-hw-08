# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.12

# Встановимо змінну середовища
ENV APP_HW /hw2

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HW

# Встановимо залежності всередині контейнера
COPY pyproject.toml poetry.lock $APP_HW/

# Встановимо poetry та залежності всередині контейнера
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 5000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "hw8.py"]