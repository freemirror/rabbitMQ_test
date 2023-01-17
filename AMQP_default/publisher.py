import pika, random, time, sys


def main(connection):
    channel = connection.channel()

    channel.queue_declare(queue='dev_queue')

    key = 0
    while True:
        value = random.randint(1000, 9999)
        key += 1
        body = f'{{{key}: {value}}}'
        channel.basic_publish(exchange='',
                              routing_key='dev_queue',
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
