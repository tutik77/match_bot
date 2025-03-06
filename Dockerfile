FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x /app/wait-for-db.sh

CMD /app/wait-for-db.sh && python manage.py migrate && python manage.py runserver & python bot.py


WORKDIR /app/bot
CMD ["python", "bot.py"]
