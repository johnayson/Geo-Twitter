from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
byte_key = ('abs').encode('utf-8')
future = producer.send('testing3', key = byte_key,value =b'fdafaqeiaarqreq')
print(future)

x = {
  "name": "John",
  "age": 30,
  "city": "San Francisco"
}

# convert into JSON:
y = json.dumps(x).encode('utf-8')

producer.send('testing3', key=b'67852', value=y)

# Block for 'synchronous' sends
try:
    print("Sending...")
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
#print ('Topic is ' + record_metadata.topic)
#print ('To partition ' + str(record_metadata.partition))
#print ('With offset ' + str(record_metadata.offset))
