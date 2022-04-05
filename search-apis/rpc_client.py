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

        # self.channel.basic_consume(
        #     queue=self.callback_queue,
        #     on_message_callback=self.on_response,
        #     auto_ack=True)
        
        self.response = {}

    def handle_response(self, corr_id, body):
        if self.corr_id != corr_id:
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
    
        for message in self.channel.consume(queue=self.callback_queue, auto_ack=True):
            method, props, body = message
            self.handle_response(props.correlation_id, body)
            logging.info(f"{len(self.response)} responses received")
            if len(self.response) >= len(pdf_uris):
                break
        
        return self.response
