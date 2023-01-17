import pika, sys


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='exc_fanout',
                             exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='exc_fanout',
                       queue=queue_name,
                       routing_key='')

    def callback(ch, method, properties, body):
        print(f'Received {body.decode()}')

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
