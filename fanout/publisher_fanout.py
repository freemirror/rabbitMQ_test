import pika, random, time, sys


def main(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange='exc_fanout',
                             exchange_type='fanout')

    key = 0
    while True:
        value = random.randint(1000, 9999)
        key += 1
        body = f'{{{key}: {value}}}'
        channel.basic_publish(exchange='exc_fanout',
                              routing_key='',
                              body=body)
        time.sleep(2)


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        main(connection)
    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()
        sys.exit(0)
