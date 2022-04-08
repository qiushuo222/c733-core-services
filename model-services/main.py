import os
import functools
import json
import logging

import pika

from feature_generation import generate_features
from model import Predictor

logging.basicConfig(level=logging.INFO)


def on_request(ch, method, props, body, model):
    body_str = body.decode("utf-8")
    try:
        pdf_uri, plaintext = json.loads(body_str)
        logging.info(f"received plaintext for uri {pdf_uri}")
        features = generate_features(plaintext)
        score = model.predict(features)
        logging.info(f"generated ranking score for uri {pdf_uri}: {score}")
    
    except Exception as e:
        logging.exception(e)
        score = -100

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
    predictor = Predictor("model_weights")

    message_callback = functools.partial(on_request, model=predictor)

    credentials = pika.PlainCredentials(mq_username, mq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=mq_host, port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue="pdf_plain_text")
    channel.basic_consume(queue='pdf_plain_text', on_message_callback=message_callback)

    logging.info(" [x] Awaiting RPC requests")
    channel.start_consuming()

if __name__ == "__main__":
    listen()
