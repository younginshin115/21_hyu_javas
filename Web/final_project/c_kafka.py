from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import dumps
from json import loads

class c_kafka:
    def From_kafka(self, topic):
        consumer = KafkaConsumer(
            topic,
            group_id=None,
            bootstrap_servers=['192.168.56.1:9092'],
            enable_auto_commit=True,
            auto_offset_reset='latest',
            value_deserializer=lambda m: loads(m))
        return consumer

    def To_kafka(self, topic, json_data):
        producer = KafkaProducer(acks=0, bootstrap_servers=['192.168.56.1:9092'],
                                 value_serializer=lambda x: dumps(x, ensure_ascii=False).encode('utf-8'))
        producer.send(topic, value=json_data)
        producer.flush()