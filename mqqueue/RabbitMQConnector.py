import pika
from utils import StreamLogger

streem_logger = StreamLogger()

class RabbitMQConnector:

    def __init__(self, **credentials):
        self.connection = None
        self.channel = None
        self.user = credentials['credentials']['mquser']
        self.password = credentials['credentials']['mqpassword']
        self.amazonmqid = credentials['credentials']['amazonmqid']
        self.region = credentials['credentials']['awsregion']

    def connect(self):
        try:
            url = f"amqps://{self.user}:{self.password}@{self.amazonmqid}.mq.{self.region}.amazonaws.com:5671"
            parameters = pika.URLParameters(url)

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            streem_logger.stream_logger.system(f"Connected :: RabbitMQ ID : {self.amazonmqid}")

        except Exception as e:
            streem_logger.stream_logger.error(f"Error connecting to RabbitMQ: {str(e)}")

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def declare_exchange(self, exchange_name, exchange_type='direct'):
        """
        Declare a RabbitMQ exchange.
        :param exchange_name: Name of the exchange.
        :param exchange_type: Type of exchange (e.g., 'direct', 'fanout', 'topic').
        """
        try:
            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=exchange_type,
                durable=True  # Make the exchange durable (it will survive server restarts)
            )
            streem_logger.stream_logger.system(f"Declared :: Exchange : {exchange_name}")

        except Exception as e:
            streem_logger.stream_logger.error(f"Error declaring exchange {exchange_name}: {str(e)}")

    def bind_queue_to_exchange(self, queue_name, exchange_name, routing_key=''):
        """
        Bind a queue to an exchange with an optional routing key.
        :param queue_name: Name of the queue.
        :param exchange_name: Name of the exchange.
        :param routing_key: Routing key for the binding (optional).
        """
        try:
            self.channel.queue_declare(queue=queue_name)
            self.channel.queue_bind(
                exchange=exchange_name,
                queue=queue_name,
                routing_key=routing_key
            )
            streem_logger.stream_logger.system(f"Bound :: Queue : {queue_name}")

        except Exception as e:
            streem_logger.stream_logger.error(f"Error binding queue {queue_name} to exchange {exchange_name}: {str(e)}")

    def publish_message(self, exchange_name, routing_key, message):
        """
        Publish a message to a RabbitMQ exchange.
        :param exchange_name: Name of the exchange.
        :param routing_key: Routing key for the message.
        :param message: Message content to be published.
        """
        try:
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message
            )
            streem_logger.stream_logger.system(f"Published Message :: Exchange {exchange_name}")

        except Exception as e:
            streem_logger.stream_logger.error(f"Error publishing message to exchange {exchange_name}: {str(e)}")

    def consume_messages(self, queue_name, callback): 
        """
        Consume messages from a RabbitMQ queue.
        :param queue_name: Name of the queue to consume from.
        :param callback: Callback function to process each received message.
        """
        try:
            def message_callback(ch, method, properties, body):
                callback(body)

            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=message_callback,
                auto_ack=True  # Automatically acknowledge received messages
            )

            streem_logger.stream_logger.system(f"Start Consuming :: Queue : {queue_name}")

            # Start consuming messages
            self.channel.start_consuming()

        except Exception as e:
            streem_logger.stream_logger.error(f"Error consuming messages from queue {queue_name}: {str(e)}")

    def delete_queue(self, queue_name):
        try:
            self.channel.queue_delete(queue=queue_name)
            streem_logger.stream_logger.system(f"Deleted :: Queue: {queue_name}")
        except Exception as e:
            streem_logger.stream_logger.error(f"Error deleting queue {queue_name}: {str(e)}")

    def delete_exchange(self, exchange_name):
        try:
            self.channel.exchange_delete(exchange=exchange_name)
            streem_logger.stream_logger.system(f"Deleted :: Exchange: {exchange_name}")
        except Exception as e:
            streem_logger.stream_logger.error(f"Error deleting exchange {exchange_name}: {str(e)}")

    def delete_routing_key(self, exchange_name, routing_key):
        try:
            self.channel.queue_unbind(exchange=exchange_name, queue='', routing_key=routing_key)
            streem_logger.stream_logger.system(f"Deleted Routing Key :: {routing_key}")
        except Exception as e:
            streem_logger.stream_logger.error(f"Error deleting routing key {routing_key} from exchange {exchange_name}: {str(e)}")
