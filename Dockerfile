FROM python:3.12-slim

# Системные зависимости: netcat (для ожидания БД), gcc и libpq-dev (для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала зависимости — так Docker кеширует слой
COPY requirements.txt requirements-prod.txt ./
RUN pip install --no-cache-dir -r requirements-prod.txt

# Копируем остальной код
COPY . .

# Делаем entrypoint исполняемым
RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]