import os
from pathlib import Path
import json
import tempfile
import threading
import logging
import functools

import requests
import pika

from PDFBoT.extractTextFrom2colHTML import getTextFrom2HTML
from PDFBoT.main import pdftohtml_test


def connect():
    mq_host = os.environ['MQ_HOST']
    mq_username = os.environ['MQ_USERNAME']
    mq_password = os.environ['MQ_PASSWORD']

    credentials = pika.PlainCredentials(mq_username, mq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=mq_host, port=5672, credentials=credentials))
    
    return connection


def pdf_to_text(filepath):
    html_path = pdftohtml_test(filepath)
    text = getTextFrom2HTML(html_path)
    return text


def download_pdf(pdf_uri_dict, fp):
    resp = requests.get(pdf_uri_dict)
    resp.raise_for_status()
    fp.write(resp.content)


def request_handler(main_connection, main_channel, delivery_tag, props, body, temp_dir):
    thread_id = threading.get_ident()
    logging.info('Thread id: {} stated working'.format(thread_id))
    
    temp_fp = tempfile.NamedTemporaryFile(suffix=".pdf", dir=temp_dir, delete=False)
    temp_pdf_path = temp_fp.name
    
    pdf_uri = body.decode("utf-8")
    logging.info(f"Thread: {thread_id} handling uri: {pdf_uri}")
    try:
        download_pdf(pdf_uri, temp_fp)
        temp_fp.close()
        paragraph_list = pdf_to_text(temp_pdf_path)
    except Exception as e:
        logging.info(f"Thread: {thread_id} uri processing failed: {pdf_uri}")
        logging.exception(e)
        response = (pdf_uri, "")
    else:
        logging.info(f"Thread: {thread_id} uri processing succeeded: {pdf_uri}")
        response = (pdf_uri, "".join(paragraph_list))
    finally:
        logging.info(f"Thread: {thread_id} message sent for uri: {pdf_uri}")
        thread_connection = connect()
        thread_channel = thread_connection.channel()
        thread_channel.basic_publish(exchange='',
                        routing_key="pdf_plain_text",
                        properties=pika.BasicProperties(
                            correlation_id = props.correlation_id, 
                            reply_to=props.reply_to),
                        body=json.dumps(response).encode("utf-8"))
        temp_fp.close()
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

        thread_connection.close()


def on_message(channel, method, properties, body, args):
    (connection, threads, temp_dir) = args
    delivery_tag = method.delivery_tag
    t = threading.Thread(target=request_handler, args=(connection, channel, delivery_tag, properties, body, temp_dir))
    t.start()
    threads.append(t)

def listen():
    logging.basicConfig(level=logging.INFO)

    connection = connect()
    channel = connection.channel()
    channel.queue_declare(queue="pdf_uri")
    channel.queue_declare(queue="pdf_plain_text")
    channel.basic_qos(prefetch_count=1)

    threads = []
    Path("output").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        on_message_callback = functools.partial(on_message, args=(connection, threads, temp_dir))
        channel.basic_consume(queue='pdf_uri', auto_ack=True, on_message_callback=on_message_callback)

        logging.info(" [x] Awaiting RPC requests")
        channel.start_consuming()

if __name__ == "__main__":
    listen()
