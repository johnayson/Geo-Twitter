import tweepy
import os
import json
import time
import datetime


with open('/Users/~/Desktop/projects/data_eng/geo_twitter/config/config.json') as data_file:
                data = json.load(data_file)
print(data)

CONSUMER_KEY = data['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = data['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = data['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = data['TWITTER_ACCESS_TOKEN_SECRET']


# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

hashes = ['#MLB','#NBA','#NFL','#NHL']
#hashes = ['#MLB']
#tweets_count = 5

def get_ts():
	timestamp = int(time.time()*1000.0)
	return timestamp

def timestamp_date(ts):
	ts = ts/1000
	return datetime.datetime.fromtimestamp(ts)	

#midpoint calculation to get the midpoint of the box
def midpoint(p1, p2):
    x = (p1[0]+p2[0])/2
    y =  (p1[1]+p2[1])/2
    return [x,y]

# Create API object
API = tweepy.API(auth)
final_tweets = {}
def get_data():
	temp_list = set()
	temp_dict = {}
	#created last hour
	
	for hash in hashes:
		print("call" + str(hash))
		for tweet in tweepy.Cursor(API.search, q = hash, result_type = "recent", tweet_mode = 'extended',wait_on_rate_limit=True).items(1000):
			#print("Fetching...")
			#print(tweet.place)
			time_lapse = datetime.datetime.utcnow() - tweet.created_at
		#has place and created last hour
			if(tweet.place != None and time_lapse < datetime.timedelta(minutes=60) ):
				point_1 = tweet.place.bounding_box.coordinates[0][0]
				point_2 = tweet.place.bounding_box.coordinates[0][2]
				center = midpoint(point_1,point_2)
				temp_dict[tweet.id] = {'tweet_id': tweet.id, 'hash' : hash,  'text' : tweet.full_text, 'location' : tweet.place.full_name, 'created_at' : tweet.created_at,'coordinate_x' : center[0], 'coordinate_y': center[1]}
				print(hash)
			
	return temp_dict #temp_list
			
def main():
	current_cnt = 0
	temp_dict = get_data()
	final_tweets.update(temp_dict)
	ts = get_ts()
	os.chdir(data['TWITTER_DIR'])
	json_file ='files/' +'tweets_' + str(ts) + '.json'
	with open(json_file, 'w') as outfile:
    		json.dump(final_tweets, outfile, sort_keys=True, indent=4,default = str)
	
main()
