from .RabbitMQConnector import RabbitMQConnector
import pickle
from utils import StreamLogger

stream_logger = StreamLogger()


class Producer():

    def __init__(self, **hyper_param) -> None:
        self.hyper_param = hyper_param
        self.run_name = hyper_param["run_name"]
        
        self.amazon_mq = RabbitMQConnector(**hyper_param)

    def publish_message_to_mq(self, message):
        exchange_name = queue_name = routing_key = f"{self.run_name}_play_data"

        self.amazon_mq.connect()
        self.amazon_mq.declare_exchange(exchange_name=exchange_name, exchange_type='direct')
        self.amazon_mq.bind_queue_to_exchange(exchange_name=exchange_name, queue_name=queue_name, routing_key=routing_key)
        self.amazon_mq.publish_message(exchange_name=exchange_name, routing_key=routing_key, message=message)

    def publish_model_to_mq(self, model, model_arch_cd):

        exchange_name = queue_name = routing_key = f"{self.run_name}_model_data"

        model_data = pickle.dumps(model)

        payload = {
            "model_arch_cd": model_arch_cd,
            "model_data": model_data
        }

        message_payload = pickle.dumps(payload)

        self.amazon_mq.connect()
        self.amazon_mq.declare_exchange(exchange_name=exchange_name, exchange_type='direct')
        self.amazon_mq.bind_queue_to_exchange(exchange_name=exchange_name, queue_name=queue_name, routing_key=routing_key)
        
        self.amazon_mq.publish_message(exchange_name=exchange_name, routing_key=routing_key, message=message_payload)
