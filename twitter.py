import tweepy
import os
import json
import time
from datetime import datetime


CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET') 
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') 

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

teams = ['#NFL']
tweets_count = 5

def get_ts():
	timestamp = int(time.time()*1000.0)
	return timestamp
def timestamp_date(ts):
	ts = ts/1000
	return datetime.fromtimestamp(ts)	

# Create API object
API = tweepy.API(auth)
final_tweets = {}
def get_data():
	temp_list = set()
	temp_dict = {}
	for tweet in tweepy.Cursor(API.search, q = teams[0], result_type = "recent", tweet_mode = 'extended').items(100):
		#print(tweet.text)
		#print(tweet.place)
		if(tweet.place != None):
			temp_dict[tweet.id] = {'tweet_id': tweet.id, 'text' : tweet.full_text, 'location' : tweet.place.full_name, 'coordinates' : tweet.place.bounding_box.coordinates}
			#print(tweet.id)
			#print(tweet.text)
			print(tweet.created_at)
			
	return temp_dict #temp_list
			
def main():
	current_cnt = 0
	while( current_cnt < tweets_count):
		temp_dict = get_data()
		current_cnt += len(temp_dict)
		final_tweets.update(temp_dict)
	print(current_cnt)
	print(final_tweets)			
	#json_tweets = json.dumps(final_tweets)
	#print(json_tweets)
	ts = get_ts()
	json_file ='files/' +'tweets_' + str(ts) + '.json'
	with open(json_file, 'w') as outfile:
    		json.dump(final_tweets, outfile, sort_keys=True, indent=4)
	
main()
ts = get_ts()
print(ts)
toDate = timestamp_date(ts)
print(toDate)
