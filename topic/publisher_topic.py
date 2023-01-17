import pika, random, time, sys, string


COLORS = ('red', 'blue', 'brown', 'black')
BRANDS = ('BMW', 'Tesla', 'Citroen', 'Audi')
CAR_BODY_STYLE = ('hatchback', 'roadster', 'sedan')


def rand_car():
    color = random.choice(COLORS)
    brand = random.choice(BRANDS)
    body_style = random.choice(CAR_BODY_STYLE)
    model = random.choice(string.ascii_lowercase) + str(random.randint(1, 99))
    return f'{brand}.{body_style}.{color}.{model}'


def main(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_exchange',
                             exchange_type='topic')

    while True:
        body = str(random.randint(1, 4))
        channel.basic_publish(exchange='topic_exchange',
                              routing_key=rand_car(),
                              body=body)
        time.sleep(1)


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        main(connection)
    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()
        sys.exit(0)
