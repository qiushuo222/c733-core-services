FROM python:3.8-buster

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .

EXPOSE 5672

CMD ["python", "main.py"]