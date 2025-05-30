FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Указываем правильный путь к manage.py
CMD ["python", "bms/manage.py", "runserver", "0.0.0.0:8000"]