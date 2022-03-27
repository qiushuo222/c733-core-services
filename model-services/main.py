import json
import logging

import pika

from feature_generation import generate_features
from model import model_mock

def on_request(ch, method, props, body):
    body_str = body.decode("utf-8")
    if body_str:
        pdf_uri, plaintext = json.loads(body_str)
        features = generate_features(plaintext)
        score = model_mock(features)
    else:
        score = 0
        logging.warning(f"empty message received")


    response = (pdf_uri, score)
    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                        props.correlation_id),
                    body=json.dumps(response).encode("utf-8"))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def listen():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="pdf_plain_text")
    channel.basic_consume(queue='pdf_plain_text', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()

if __name__ == "__main__":
    listen()
