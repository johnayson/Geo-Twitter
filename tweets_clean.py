import twitter as tweets
import re



print(tweets.final_tweets)

raw_tweets = tweets.final_tweets
#Data Cleanup
def clean_tweets(text):
	#remove emojis
	#text = text.encode('ascii','ignore').decode('ascii')
	#remove urls
	#text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	return text

for key in raw_tweets:
	clean_tweet = clean_tweets(raw_tweets[key]['text'])
	print(clean_tweet)
	print("\n")
