
import os
import pika
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv("RABBITMQ_URL")

if not url:
    raise ValueError("RABBITMQ_URL not found!")

try:
    print("Connecting to CloudAMQP...")

    params = pika.URLParameters(url)

    params.heartbeat = 60
    params.connection_attempts = 2
    params.socket_timeout = 15
    params.stack_timeout = 20
    params.blocked_connection_timeout = 30

    connection = pika.BlockingConnection(params)

    print("SUCCESS: Connected to RabbitMQ!")

    channel = connection.channel()

    channel.exchange_declare(
        exchange="rapido-dispatch",
        exchange_type="topic",
        durable=True
    )

    print("SUCCESS: Topic exchange declared!")

    connection.close()

    print("Connection closed successfully.")

except Exception as e:

    print("CONNECTION FAILED")
    print("Exception:", type(e).__name__)
    print("Details:", repr(e))
