import csv

#third-party library in requirements.txt
import twitter 
from local_settings import *

def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

def grab_tweets(api, max_id=None):
    source_tweets=[]
    user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=False)
    if user_tweets:
        max_id = user_tweets[-1].id-1
        for tweet in user_tweets:
#        tweet.text = filter_tweet(tweet)
            if len(tweet.text) != 0:
                source_tweets.append(tweet)
    else:
        max_id = None
    return source_tweets, max_id

def filter_tweet(tweet):
    tweet.text = re.sub(r'\b(RT|MT) .+','',tweet.text) #take out anything after RT or MT
    tweet.text = re.sub(r'(\#|@|(h\/t)|(http))\S+','',tweet.text) #Take out URLs, hashtags, hts, etc.
    tweet.text = re.sub(r'\n','', tweet.text) #take out new lines.
    tweet.text = re.sub(r'\"|\(|\)', '', tweet.text) #take out quotes.
    tweet.text = re.sub(r'\xe9', 'e', tweet.text) #take out accented e
    tweet.text = re.sub(r'\&amp;', '&', tweet.text) #clean up escaped html ampersands
    return tweet
    
def set_max(file): 
    mylist = []
    myfile = file
    with open(myfile, 'r') as csvfile:
        myreader = csv.reader(csvfile)
        for row in myreader:
            mylist.append(row)
    max_id = mylist[1][1]
    return max_id

if __name__=="__main__":
    user=SOURCE_ACCOUNT
    source_tweets = []
    new_tweets = []
    api=connect()
    try:
        file = OUTPUT
        read = open(file).read()
        max_id = set_max(file)
        print "Updating old file"
    except:
        print "Creating new file"
        max_id = None
        header = ['created_at', 'tweet_id', 'status_text', 'location', 'coordinates']
        with open(OUTPUT,'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)
            csvfile.close()
        pass
    new_tweets, max_id=grab_tweets(api, max_id)
    source_tweets += new_tweets
    while max_id is not None:
        new_tweets, max_id=grab_tweets(api, max_id)
        source_tweets += new_tweets
    if len(source_tweets) == 0:
        print "Error fetching tweets from Twitter. Aborting."
        print "Have you specified a target account in local_settings.py?"
        sys.exit()
    print "{0} tweets found".format(len(source_tweets))

    for tweet in source_tweets:
        row = [tweet.created_at, tweet.id, tweet.text.encode('utf-8'), tweet.location, tweet.coordinates]
        with open(OUTPUT,'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row)
            csvfile.close()
