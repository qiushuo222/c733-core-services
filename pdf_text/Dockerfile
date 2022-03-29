FROM python:3.8

WORKDIR /code

COPY requirements.txt .

COPY PDFBoT/ .

COPY *.py .

RUN pip install --no-cache-dir -r requirements.txt

COPY dependencies/libjpeg-turbo8_amd64.deb .

RUN apt install ./libjpeg-turbo8_amd64.deb

COPY dependencies/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb .

RUN apt update && apt -y upgrade && apt -y --no-install-recommends install ./pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb

EXPOSE 5672

CMD ["python", "main.py"]
