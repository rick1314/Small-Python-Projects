import tweepy
import time
from random import *

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

query = 'T-Series -filter:retweets'
replies = 'replies.txt'
replied = 'replied.txt'
max_tweets = 100

def test():
	user = api.me()
	print (user.name)

def searchNreply():
	searched_tweets = []
	last_id = -1
	print("\nStarting Tweet Search")
	while len(searched_tweets) < max_tweets:

		count = max_tweets - len(searched_tweets)
		try:
			new_tweets = api.search(q=query, count=count, geocode="19.103556,72.888072,150km", max_id=str(last_id - 1))
			if not new_tweets:
				break
			searched_tweets.extend(new_tweets)
			last_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			# depending on TweepError.code, one may want to retry or wait
			# to keep things simple, we will give up on an error
			print("\nThere was a Tweepy error")
			break
			
		print("\nFound %d Tweets"%len(searched_tweets))
	print("\nDone Searching Tweets")
	return searched_tweets
	
def sleepingTime():
	print("\nSleeping for 5 minutes")
	time.sleep(300)

def tweetEmAll(tweets):
	file = open(replies, 'r') #just read
	rfile = open(replied, 'r+') #read and append
	lines=file.readlines()
	file.seek(0)
	num = sum(1 for _ in file)
	# n = randint(1, num) 
	# print("Sum: %d Num: %d Line: %s"%(num,n,lines[n-1]))  #while n gives us the line number in a array the positions start form 0

	me = api.me()
	total = me.statuses_count
	
	for tweet in tweets:
		n = randint(1, num) 
		phrase = lines[n-1]
		tweetList = rfile.readlines()
		try:
			tweetId = tweet.id
			username = tweet.user.screen_name
			if(str(tweetId) in tweetList):
				print("\nAlready Tweeted to:",tweetId)
			else:
				total = total + 1
				api.update_status("Hello @" + username + ", " + phrase + " #"+str(total+1), in_reply_to_status_id = tweetId)
				print ("\nReplied with " + phrase)
				rfile.write(str(tweetId)+"\n")
				#print("Sleeping for 2.5 minutes")
				#print(api.rate_limit_status())
				#time.sleep(150)
		except tweepy.TweepError as e:
			print(e.reason)
			break
	rfile.close()
	file.close()

def main():

	while(True):
		test()
		tweets = searchNreply()
		tweetEmAll(tweets)
		sleepingTime()

if __name__ == '__main__':
	main()