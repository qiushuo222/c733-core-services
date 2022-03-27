from pathlib import Path
import json
import tempfile
import logging

import requests
import pika

from PDFBoT.extractTextFrom2colHTML import getTextFrom2HTML
from PDFBoT.main import pdftohtml_test


def pdf_to_text(filepath):
    html_path = pdftohtml_test(filepath)
    text = getTextFrom2HTML(html_path)
    return text


def download_pdf(pdf_uri_dict, fp):
    resp = requests.get(pdf_uri_dict)
    resp.raise_for_status()
    fp.write(resp.content)


def request_handler_factory(temp_dir):

    def request_handler(ch, method, props, body):
        temp_fp = tempfile.NamedTemporaryFile(suffix=".pdf", dir=temp_dir, delete=False)
        temp_pdf_path = temp_fp.name
        
        pdf_uri = body.decode("utf-8")
        try:
            download_pdf(pdf_uri, temp_fp)
            temp_fp.close()
            paragraph_list = pdf_to_text(temp_pdf_path)
        except Exception as e:
            logging.exception(e)
            response = (pdf_uri, "")
        else:
            response = (pdf_uri, "".join(paragraph_list))
        finally:
            ch.basic_publish(exchange='',
                            routing_key="pdf_plain_text",
                            properties=pika.BasicProperties(
                                correlation_id = props.correlation_id, 
                                reply_to=props.reply_to),
                            body=json.dumps(response).encode("utf-8"))
            ch.basic_ack(delivery_tag=method.delivery_tag)
            temp_fp.close()
            Path(temp_pdf_path).unlink(missing_ok=True)

    return request_handler

def listen():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="pdf_uri")
    channel.queue_declare(queue="pdf_plain_text")
    Path("output").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        on_request = request_handler_factory(temp_dir)
        channel.basic_consume(queue='pdf_uri', on_message_callback=on_request)

        print(" [x] Awaiting RPC requests")
        channel.start_consuming()

if __name__ == "__main__":
    listen()