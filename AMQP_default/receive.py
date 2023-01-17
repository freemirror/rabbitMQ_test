import pika, sys


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='dev_queue')

    def callback(ch, method, properties, body):
        print(f'Received {body.decode()}')

    channel.basic_consume(queue='dev_queue',
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
