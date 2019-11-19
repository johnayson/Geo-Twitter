#import twitter as tweets
import re
import json
import glob

#print(tweets.final_tweets)

#raw_tweets = tweets.final_tweets
#Data Cleanup
def clean_tweets(text):
	#remove emojis
	text = text.encode('ascii','ignore').decode('ascii')
	#remove urls
	text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	return text
def dict_to_json(this_dict,name):
	str_json = 'ref_' + name
	with open(str_json, 'w') as outfile:
                json.dump(this_dict, outfile, sort_keys=True, indent=4)
		
def refine(name):
	with open(name) as data_file:    
		data = json.load(data_file)
		print(data)
	for keys in data:
		data[keys]['text'] = clean_tweets(data[keys]['text'])
	print(data)
	dict_to_json(data,name)



refine('read.json')
#files = glob.glob('*.json')
#print(files)
