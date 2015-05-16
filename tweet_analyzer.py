# Python code to stream some number of tweets containing some keyword 
# (set keyword(s) and number of tweets in first block below).
#
# Performs a simple sentiment analysis, and prints summary including 
# tweet location (if user made that info available).
#
# User must include their own Twitter tokens/keys below.
#==============================================
# SET THESE VARIABLES:

#KEYWORD(S) TO LOOK FOR?
#query = 'snow OR snowing OR snowflakes'
#query = 'powder AND mountain'
query = 'cat'

#HOW MANY TWEETS?
num_tweets = 10

#PERSONAL TWITTER APPLICATION TOKENS/KEYS?
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#==============================================

#from tweepy import Stream
#from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener

#import csv

import tweepy
import urllib2
import json
import re
import unicodedata

#LINK TO ANALYZE SENTIMENT:
url_sentiment = 'http://text-processing.com/api/sentiment/'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)#, secure=True)


#==============================================


# can use .items or .pages to limit # tweets returned

for tw in tweepy.Cursor(api.search, q=query, lang='en', monitor_rate_limit=True, wait_on_rate_limit=True).items(num_tweets):

    #tweet = re.sub('[@#$]', '', tw.text)
    #tweet = tweet.replace("\\", '')
    #tweet = ''.join([ c if (c.isalnum() or c=='?' or c=='!') else ' ' for c in tw.text])

    try:
        tweet = unicodedata.normalize('NFKD', tw.text).encode('ascii','ignore')
    except:
        tweet = tw.text

    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub(r'[@#$]', '', tweet)

    print '\n-----------\n'
    #print tw.text, '\n'
    print tweet, '\n'
    
    req = urllib2.Request(url_sentiment, 'text='+tweet)
    response = json.load(urllib2.urlopen(req))

    sentiment = response['label']
    neg = response['probability']['neg']
    pos = response['probability']['pos']
    neut = response['probability']['neutral']

    print 'SENTIMENT: ', sentiment#, '\n', 
    print '     positive: ', pos
    print '     negative: ', neg
    print '     neutral: ', neut

    user = tw._json['user']
    if tw._json['coordinates'] != None:
        print '\n\n', tw._json['coordinates']['coordinates'][0]
        print tw._json['coordinates']['coordinates'][1], '\n\n'
    else:
        print 'coord: ', tw._json['coordinates']

    print '\nLOCATION: ', user['location']  
    print 'TIMEZONE: ', user['time_zone']
    try:
        place = tw._json['place']['full_name']
    except:
        place = 'None Given'
    print 'PLACE: ', place
    #print 'HASHTAGS: ', tw._json['entities']['hashtags']

print '\n-----------\n'

#it._json is a dict, which in turn contains the dict it._json['user']
#prints all dict keys: it._json.keys()

################################################################

#-----------
#stuff I copied from a helpful blog post:
#http://sachithdhanushka.blogspot.ca/2014/02/mining-twitter-data-using-python.html

class TweetListener(tweepy.StreamListener):
    def on_data(self, data):
        #print type(json.loads(data)) #dict
        print data #str
        return True
    def on_error(self, status):
        print status

#    def on_status(self, status):
#        with open('file.txt', 'w') as f: 
#            f.write('Author,Date,Text')
#            writer = csv.writer(f)
#            writer.writerow([status.author.screen_name, status.created_at, status.text])

#2nd line prints constant tweets regarding 'cats' (control-C to quit)

#stream = tweepy.streaming.Stream(auth, TweetListener())
#stream.filter(track=['cats'])

#-----------

class TweetListen_byJes(tweepy.StreamListener):
    def on_data(self, data):
        j = json.loads(data) #dict
        print j['text']
        return True
    def on_error(self, status):
        print status

#stream = tweepy.streaming.Stream(auth, TweetListen_byJes())
#stream.filter(track=['cats'])

#-----------

#I think this is equivalent to Cursor method above
#mysearch = api.search(q='cats',count=10) 
#,include_rts=False) #to not include native retweets...
#for c in mysearch:
#    print '\n', c.text

#mysearch[0].text
#mysearch[0].retweets
#mysearch[0].entities
