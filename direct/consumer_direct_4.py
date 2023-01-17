import pika, sys


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='rout_mess',
                             exchange_type='direct')

    queue_name = 'all'
    channel.queue_declare(queue=queue_name, exclusive=True)

    channel.queue_bind(exchange='rout_mess',
                       queue=queue_name,
                       routing_key='warnings')

    channel.queue_bind(exchange='rout_mess',
                       queue=queue_name,
                       routing_key='errors')

    channel.queue_bind(exchange='rout_mess',
                       queue=queue_name,
                       routing_key='infos')

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
