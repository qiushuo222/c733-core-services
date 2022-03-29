FROM python:3.8-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

CMD gunicorn -w 4 -b 0.0.0.0:8000 "app:app"