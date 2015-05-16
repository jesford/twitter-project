# Python code to stream some number of tweets containing some keyword 
# (set keyword(s) and number of tweets in first block below).
#
# Performs a simply sentiment analysis, prints summary, and
# plots color-coded positive/negative tweets on a map.
# [green = positive; yellow = neutral; red = negative].
#
# User must include their own Twitter tokens/keys below.
#==============================================
# SET THESE VARIABLES:

#KEYWORD(S) TO LOOK FOR?
#query = 'snow OR snowing OR snowflakes'
#query = 'powder AND mountain'
query = 'cat'

#HOW MANY TWEETS?
#note: depending on query and num_tweets, program may take a
#while... start with just a few (maybe 10) and then increase.
#Limiting factor is lack of geographical info for the tweets.
num_tweets = 10

#PERSONAL TWITTER APPLICATION TOKENS/KEYS?
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
#==============================================

import tweepy
import urllib2
import json
import re
import unicodedata

#ANALYZE SENTIMENT:
url_sentiment = 'http://text-processing.com/api/sentiment/'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#==============================================

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

#map set up

NE_lat = 60.
NE_long = -50.
SW_lat = 10.
SW_long = -120.
center_lat = 30.
center_long = -75.

m = Basemap(projection='laea', lat_0=center_lat, lon_0=center_long, resolution = 'l', llcrnrlon=SW_long, urcrnrlon=NE_long, llcrnrlat=SW_lat, urcrnrlat=NE_lat)

m.drawcoastlines()
m.drawmapboundary(color='black', linewidth=3., fill_color='cyan')
m.fillcontinents(color='lightgray',lake_color='cyan')

m.drawstates()
m.drawcountries(linewidth=2.)

#==============================================

count = 0

for tw in tweepy.Cursor(api.search, q=query, lang='en', monitor_rate_limit=True, wait_on_rate_limit=True).items():

    # if no coordinates, skip to next tweet
    if tw._json['coordinates'] == None:
        continue

    coord = tw._json['coordinates']['coordinates']
    longitude = coord[0]
    latitude = coord[1]

    # if coordinates outside map range, skip to next tweet
    if (longitude > NE_long) or (longitude < SW_long) or (latitude > NE_lat) or (latitude < SW_lat):
        continue

    count += 1
    print 'count ', count

    # convert tweet junk and print some info to screen...

    try:
        tweet = unicodedata.normalize('NFKD', tw.text).encode('ascii','ignore')
    except:
        tweet = tw.text
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub(r'[@#$]', '', tweet)

    print '\n-----------\n'
    #print tw.text, '\n'
    print tweet, '\n'

    user = tw._json['user']

    print '\nLOCATION: ', user['location']  
    try:
        place = tw._json['place']['full_name']
    except:
        place = 'None Given'
    print 'PLACE: ', place
    print 'LONG, LAT: ', longitude, latitude


    # get sentiment of queried tweets...

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

    if neut > 0.5:
        dotcolor = 'yellow'
    elif pos >= 0.5:
        dotcolor = 'green'
    else:
        dotcolor = 'red'

    # plot color-coded sentiment tweets
    m.scatter(longitude, latitude, color=dotcolor, s=50, latlon=True, zorder=2)

    if count >= num_tweets:
        break
