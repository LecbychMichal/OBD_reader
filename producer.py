from confluent_kafka import Producer
import json
import logging
import obd
import argparse
import time
from typing import List


logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

p=Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer initiated:')

def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = f'Produced message {msg.topic()} with value {msg.value().decode("utf-8")}' 
        logger.info(message)
        print(message)


def main(speed: float, voltage: float, dtc: List[str], args):
    """
    Query is done by OBD protocol.
    Each DTC is represented by a tuple containing the DTC code, and a description.
    For commands that return multiple DTCs, a list is used.
    Producer is used to supply data for consumers

    """
    limit = args.limit
    pause = args.pause
    i = 0
    trouble_codes = {}

    while i < limit:
        response_speed = connection.query(speed)
        response_voltage = connection.query(voltage)
        codes = connection.query(dtc)
        codes_value = codes.value

        if len(codes_value) == 0:
            trouble_codes = None
        elif len(codes_value) == 2:
            trouble_codes[codes_value[0]] = codes_value[1]
        else:
            for code, val in codes_value:
                trouble_codes[code] = val


        data={
           'speed': response_speed.value.magnitude,
           'voltage': response_voltage.value.magnitude,
           'trouble_codes': trouble_codes
           }

        m=json.dumps(data)
        p.poll(1)
        p.produce('OBD-tracker', m.encode('utf-8'),callback=receipt)
        p.flush()
        time.sleep(pause)
        i += 1

        
if __name__ == '__main__':
    """
    limit - maximum number of messages pushed by producer
    pause - time between each query
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default="5")
    parser.add_argument('--pause', type=float, default="0.5")
    args = parser.parse_args()
    
    connection = obd.OBD('/dev/pts/3', timeout=100)
    speed = obd.commands.SPEED
    voltage = obd.commands.ELM_VOLTAGE
    dtc = obd.commands.GET_DTC
    main(speed, voltage, dtc, args)