import os
import subprocess
import logging
import tempfile
import json

import requests
from kafka import KafkaConsumer, KafkaProducer
from main import pdftohtml_test
from extractTextFrom2colHTML import getTextFrom2HTML


def pdf_to_text(filepath):
    html_path = pdftohtml_test(filepath)
    text = getTextFrom2HTML(html_path)
    return text


def download_pdf(pdf_uri_dict, fp):
    resp = requests.get(pdf_uri_dict)
    resp.raise_for_status()
    fp.write(resp.content)


def listen(c_topic, p_topic):
    consumer = KafkaConsumer(c_topic)
    producer = KafkaProducer()
    for message in consumer:
        uri = message.value.decode('utf-8')
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_fp = tempfile.NamedTemporaryFile(suffix=".pdf", dir=tmp_dir, delete=False)
            tmp_pdf_path = tmp_fp.name
            try:
                download_pdf(uri, tmp_fp)
                tmp_fp.close()
                fulltext = pdf_to_text(tmp_pdf_path)
            except Exception as e:
                logging.exception(e)
            else:
                producer.send(p_topic, value=json.dumps(fulltext).encode("utf-8"))


if __name__ == "__main__":
    listen("raw_pdf_uri", "plaintext_pdf")
