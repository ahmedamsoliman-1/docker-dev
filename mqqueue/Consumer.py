from .RabbitMQConnector import RabbitMQConnector
import os
import torch
import pickle
# import threading
from utils import StreamLogger
stream_logger = StreamLogger()


class Consumer():

    def __init__(self, **hyper_param) -> None:
        self.hyper_param = hyper_param
        self.run_name = hyper_param["run_name"]
        self.exchange = self.run_name
        self.routing_key = self.run_name
        self.queue = self.run_name
        self.amazon_mq = RabbitMQConnector(**hyper_param)
        self.count = 0

    def consumer_callback(self, message):
        received_tensors = pickle.loads(message)
        received_game_id = received_tensors[0]
        received_states = received_tensors[1]
        received_probabilities = received_tensors[2]
        received_comb_winner_rewards = received_tensors[3]
        received_run_name = received_tensors[4]
        #received_generation_number = received_tensors[5]

        train_data_folder = os.path.join(
            self.hyper_param["cache_folder"], "data", received_game_id)
        os.makedirs(train_data_folder, exist_ok=True)
        torch.save(received_states, os.path.join(
            train_data_folder, "states.pt"))
        torch.save(received_probabilities, os.path.join(
            train_data_folder, "probs.pt"))
        torch.save(received_comb_winner_rewards,
                os.path.join(train_data_folder, "rewards.pt"))
        self.count = self.count+1
        stream_logger.stream_logger.system(
            f"The game consumed by RabbitMQ for game id:{received_game_id},run name:{received_run_name},total count:{self.count}")

    def game_data_consumer(self):

        exchange_name = queue_name = routing_key = f"{self.run_name}_play_data"
        self.amazon_mq.connect()
        self.amazon_mq.bind_queue_to_exchange(self.queue, self.exchange, routing_key=self.routing_key)
        self.amazon_mq.consume_messages(self.queue, self.consumer_callback)

    # def model_data_consumer(self):
        
    #     exchange_name = queue_name = routing_key = f"{self.run_name}_model_data"
    #     # Consume models from a different queue
    #     self.amazon_mq.connect()
    #     self.amazon_mq.bind_queue_to_exchange(
    #         queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)  # Bind to the same exchange as game data
    #     self.amazon_mq.consume_messages(queue_name, self.model_data_consumer_callback)
