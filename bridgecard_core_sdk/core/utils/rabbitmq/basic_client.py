import ssl
import pika
import logging

class BasicPikaClient:

    def __init__(
            self,
            rabbitmq_broker_id: str,
            rabbitmq_user: str,
            rabbitmq_password: str,
            region: str,
            environment: str = "production",
    ):

        environment = environment.lower()

        if environment == "local":
            # Local RabbitMQ (e.g., running via Docker)
            host = rabbitmq_broker_id or "localhost"
            port = 5672
            url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{host}:{port}/"
            parameters = pika.URLParameters(url)
            logging.info(f"[BasicPikaClient] Environment: local — connecting to {url}")

        else:
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
            url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671"
            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)
            logging.info(f"[BasicPikaClient] Environment: production — connecting to {url}")

        # Establish connection
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()