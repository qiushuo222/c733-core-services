FROM python:3.7.11-stretch

WORKDIR /code

COPY requirements.txt .

COPY PDFBoT/ ./PDFBoT

COPY *.py .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt -y --no-install-recommends install pdf2htmlex=0.14.6+ds-3

EXPOSE 5672

CMD ["python", "main.py"]
