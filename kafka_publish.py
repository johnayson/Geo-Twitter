#import twitter as tweets
import re
import json
import glob
import os
from pathlib import Path
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json


with open('/Users/~/Desktop/projects/data_eng/geo_twitter/config/config.json') as data_file:
                data = json.load(data_file)

def kafka_send(topic,key,json_payload):
	producer = KafkaProducer(bootstrap_servers = ['localhost:9092'])
	payload = json.dumps(json_payload).encode('utf-8')
	key_bytes = key.encode('utf-8')
	value_bytes = json.dumps(json_payload).encode('utf-8')
	sent_response = producer.send(topic, key = key_bytes, value = value_bytes)
	try:
		print("Sending...")
		record_metadata = sent_response.get(timeout=10)
	except KafkaError:
	    # Decide what to do if produce request failed...
		log.exception()
		pass

	#Successful result returns assigned partition and offset
	print ('Topic is ' + record_metadata.topic)
	print ('To partition ' + str(record_metadata.partition))
	print ('With offset ' + str(record_metadata.offset))

#print(tweets.final_tweets)

def kafka_publish(file,topic):
	
	with open(file) as data_file:
                data = json.load(data_file)
                print(data)

	for key in data:
		print(key)
		kafka_send(topic,str(key),data[key])
		

os.chdir(data['TWITTER_DIR'])
path = Path('files/')
x = list(path.rglob('*.json'))
print(x)
for i in x:
	print(i)

files = glob.glob('files/ref_*.json')
print(files)
for refine_file in files:
	#success,refine_file=refine(file) 
	#if(success == True):
	#Publish successfully cleaned file,sends only filename
	kafka_publish(refine_file,'testing3')
	#done_str = 'mv '+ file + ' '  +file + '.done'
	print(refine_file)
	#print(success)
	#os.system(done_str)

#x = {
#  "name": "Sample_John",
#  "age": 30,
#  "city": "San Francisco"
#}

#kafka_send('testing3','123456',x)

