#import twitter as tweets
import re
import json
import glob
import os
from pathlib import Path

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
	str_json = 'files/' + 'ref_' + name
	with open(str_json, 'w') as outfile:
                json.dump(this_dict, outfile, sort_keys=True, indent=4)
		
def refine(name):
	with open(name) as data_file:    
		print(name)
		data = json.load(data_file)
		print(data)
	for keys in data:
		data[keys]['text'] = clean_tweets(data[keys]['text'])
	print(data)
	dict_to_json(data,os.path.basename(name))
	return True

path = Path('files/')
x = list(path.rglob('*.json'))
print(x)
for i in x:
	print(i)

files = glob.glob('files/*.json')
print(files)
for file in files:
	success=refine(file) 
	if(success == True):
		done_str = 'mv '+ file + ' '  +file + '.done'
		print(file)
		print(success)
		os.system(done_str)
