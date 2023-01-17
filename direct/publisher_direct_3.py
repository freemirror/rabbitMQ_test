import pika, random, time, sys


def main(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange='rout_mess',
                             exchange_type='direct')

    while True:
        code = random.randint(100, 999)
        body = f'Info message {code}'
        channel.basic_publish(exchange='rout_mess',
                              routing_key='infos',
                              body=body)
        time.sleep(6)


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        main(connection)
    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()
        sys.exit(0)
