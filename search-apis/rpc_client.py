import uuid
import json

import pika

class PDFRankingClient():

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

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

    def call(self, pdf_uris):
        self.corr_id = str(uuid.uuid4())
        for uri in pdf_uris:
            self.channel.basic_publish(
                exchange='',
                routing_key='pdf_uri',
                properties=pika.BasicProperties(
                    reply_to=self.callback_queue,
                    correlation_id=self.corr_id),
                body=uri
            )
        
        while len(self.response) < len(pdf_uris):
            self.connection.process_data_events()
        
        return self.response
