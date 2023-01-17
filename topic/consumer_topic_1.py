import pika, sys


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_exchange',
                             exchange_type='topic')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='topic_exchange',
                       queue=queue_name,
                       routing_key='*.*.blue.#')

    def callback(ch, method, properties, body):
        print(f'Received {method.routing_key} {body.decode()}')

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
