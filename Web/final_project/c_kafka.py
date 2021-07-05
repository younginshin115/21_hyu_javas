# -*- coding: utf-8 -*-

from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import dumps
from json import loads

kafka_url = "23.96.54.46:9092"

class c_kafka:
    def From_kafka(self, topic):
        consumer = KafkaConsumer(
            topic,
            group_id=None,
            bootstrap_servers=[kafka_url],
            enable_auto_commit=True,
            auto_offset_reset='latest',
            #heartbeat_interval_ms=8000,
            value_deserializer=lambda m: loads(m))
        return consumer

    def To_kafka(self, topic, json_data):
        producer = KafkaProducer(acks=0, bootstrap_servers=[kafka_url],
                                 value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'))
        producer.send(topic, value=json_data)
        producer.flush()