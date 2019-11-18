import tweepy
import os

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET') 
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET') 

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

teams = ['#NFL']
tweets_count = 5


# Create API object
API = tweepy.API(auth)
final_tweets = {}
def getData():
	temp_list = set()
	temp_dict = {}
	for tweet in tweepy.Cursor(API.search, q = teams[0], result_type = "recent", tweet_mode = 'extended').items(100):
		#print(tweet.text)
		#print(tweet.place)
		if(tweet.place != None):
			temp_dict[tweet.id] = {'tweet_id': tweet.id, 'text' : tweet.full_text, 'location' : tweet.place.full_name, 'coordinates' : tweet.place.bounding_box.coordinates}
			#print(tweet.id)
			#print(tweet.text)
			#print(tweet.place)
			
	return temp_dict #temp_list
			
def main():
	current_cnt = 0
	while( current_cnt < tweets_count):
		temp_dict = getData()
		current_cnt += len(temp_dict)
		final_tweets.update(temp_dict)
	print(current_cnt)
	print(final_tweets)			

main()
