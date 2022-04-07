import os
from pathlib import Path
import json
import tempfile
import logging
import functools
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

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


def request_handler(props, body, temp_dir):
    pid = os.getpid()
    logging.info('Process id: {} stated working'.format(pid))
    
    temp_fp = tempfile.NamedTemporaryFile(suffix=".pdf", dir=temp_dir, delete=False)
    temp_pdf_path = temp_fp.name
    
    pdf_uri = body.decode("utf-8")
    logging.info(f"PID: {pid} handling uri: {pdf_uri}")
    try:
        download_pdf(pdf_uri, temp_fp)
        temp_fp.close()
        paragraph_list = pdf_to_text(temp_pdf_path)
    except Exception as e:
        logging.info(f"PID: {pid} uri processing failed: {pdf_uri}")
        logging.exception(e)
        response = (pdf_uri, "")
    else:
        logging.info(f"PID: {pid} uri processing succeeded: {pdf_uri}")
        response = (pdf_uri, "".join(paragraph_list))
    finally:
        logging.info(f"PID: {pid} message sent for uri: {pdf_uri}")
        process_connection = connect()
        process_channel = process_connection.channel()
        process_channel.basic_publish(exchange='',
                        routing_key="pdf_plain_text",
                        properties=pika.BasicProperties(
                            correlation_id = props.correlation_id, 
                            reply_to=props.reply_to),
                        body=json.dumps(response).encode("utf-8"))
        temp_fp.close()
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

        process_connection.close()


def ack_message(channel, delivery_tag, _future):
    channel.basic_ack(delivery_tag=delivery_tag)



def listen():
    logging.basicConfig(level=logging.INFO)

    connection = connect()
    channel = connection.channel()
    channel.queue_declare(queue="pdf_uri")
    channel.queue_declare(queue="pdf_plain_text")
    # channel.basic_qos(prefetch_count=1)

    Path("output").mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir, ProcessPoolExecutor(multiprocessing.cpu_count()) as executor:
        logging.info(" [x] Awaiting RPC requests")
        for message in channel.consume(queue='pdf_uri', auto_ack=True):
            method, properties, body = message
            future = executor.submit(request_handler, properties, body, temp_dir)
            # ack_message_callback = functools.partial(ack_message, channel, method.delivery_tag)
            # future.add_done_callback(ack_message_callback)

if __name__ == "__main__":
    listen()
