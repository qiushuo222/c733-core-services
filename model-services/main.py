import os
import json
import logging

import pika

from feature_generation import generate_features
from model import model_mock

logging.basicConfig(level=logging.INFO)


def on_request(ch, method, props, body):
    body_str = body.decode("utf-8")
    try:
        logging.info(f"processing plaintext")
        pdf_uri, plaintext = json.loads(body_str)
        features = generate_features(plaintext)
        score = model_mock(features)
    
    except Exception as e:
        logging.exception(e)
        score = 0
    
    finally:
        response = (pdf_uri, score)
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=json.dumps(response).encode("utf-8"))
        ch.basic_ack(delivery_tag=method.delivery_tag)


def listen():
    mq_host = os.environ['MQ_HOST']
    mq_username = os.environ['MQ_USERNAME']
    mq_password = os.environ['MQ_PASSWORD']

    credentials = pika.PlainCredentials(mq_username, mq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=mq_host, port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue="pdf_plain_text")
    channel.basic_consume(queue='pdf_plain_text', on_message_callback=on_request)

    logging.info(" [x] Awaiting RPC requests")
    channel.start_consuming()

if __name__ == "__main__":
    listen()
