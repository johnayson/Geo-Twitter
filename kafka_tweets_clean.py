#import twitter as tweets
import re
import json
import glob
import os
from pathlib import Path
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

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

#raw_tweets = tweets.final_tweets
#Data Cleanup
with open('/Users/~/Desktop/projects/data_eng/geo_twitter/config/config.json') as data_file:
                data = json.load(data_file)
#print(data)

def clean_tweets(text):
	#remove emojis
	text = text.encode('ascii','ignore').decode('ascii')
	#remove urls
	text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	return text
def dict_to_json(this_dict,name):
	str_json = 'files/' + 'ref_' + name
	with open(str_json, 'w') as outfile:
                json.dump(this_dict, outfile, sort_keys=True, indent=4)
	return str_json
		
def refine(name):
	with open(name) as data_file:    
		print(name)
		data = json.load(data_file)
		print(data)
	for keys in data:
		try:
			data[keys]['text'] = clean_tweets(data[keys]['text'])
		except:
			print("Error in cleaning tweets data")
			sys.exit(1)
	print("The Json data is")
	print(data)
	#Once the whole file has been cleaned
	#kafka_publish('testing3',data)
	refine_file = dict_to_json(data,os.path.basename(name))
	return True,refine_file

#Individually publishes each tweet of the refined/cleaned file to kafka 
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

files = glob.glob('files/*.json')
print(files)
for file in files:
	success,refine_file=refine(file) 
	if(success == True):
		#Publish successfully cleaned file,sends only filename
		kafka_publish(refine_file,'testing3')
		done_str = 'mv '+ file + ' '  +file + '.done'
		print(file)
		print(success)
		os.system(done_str)

#x = {
#  "name": "Sample_John",
#  "age": 30,
#  "city": "San Francisco"
#}

#kafka_send('testing3','123456',x)

