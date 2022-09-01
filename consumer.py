
from confluent_kafka import Consumer


print('Kafka Consumer initiated:')
c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
c.subscribe(['OBD-tracker'])

def main():
    while True:
        msg=c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        print(data)
    c.close()
        
if __name__ == '__main__':
    main()