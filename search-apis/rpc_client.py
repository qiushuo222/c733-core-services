import uuid
import json
import logging

import os

import pika
import redis

logging.basicConfig(level=logging.INFO)

class PDFRankingClient():

    def __init__(self):
        mq_host = os.environ['MQ_HOST']
        mq_username = os.environ['MQ_USERNAME']
        mq_password = os.environ['MQ_PASSWORD']

        redis_host = os.environ["REDIS_HOST"]

        self.redis = redis.Redis(host=redis_host, port=6379, db=0)

        credentials = pika.PlainCredentials(mq_username, mq_password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=mq_host, port=5672, credentials=credentials))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="pdf_uri")
        result_queue = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result_queue.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        
        self.response = {}

    def on_response(self, ch, method, props, body):
        if self.corr_id != props.correlation_id:
            return
        pdf_uri, score = json.loads(body.decode("utf-8"))
        self.response[pdf_uri] = score
        self.redis.set(pdf_uri, score)

    def call(self, pdf_uris):
        self.corr_id = str(uuid.uuid4())
        existing_scores = self.redis.mget(pdf_uris)
        for i, uri in enumerate(pdf_uris):
            if existing_scores[i]:
                self.response[uri] = float(existing_scores[i].decode("utf-8"))
            else:
                self.channel.basic_publish(
                    exchange='',
                    routing_key='pdf_uri',
                    properties=pika.BasicProperties(
                        reply_to=self.callback_queue,
                        correlation_id=self.corr_id),
                    body=uri
                )
        
        while len(self.response) < len(pdf_uris):
            logging.info(f"{len(self.response)} responses received")
            self.connection.process_data_events()
        
        return self.response
