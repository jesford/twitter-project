## Twitter Streaming and Analysis

This is some code I wrote to stream tweets, query for keywords (like cats, or fresh snow, etc), and analyze sentiment. This was a project I worked on for a "Databases and Big Data" small group breakout of the Vancouver, BC Girl-Dev Meetup group. There are two sets of code:

- **tweet_analyzer.py** streams tweets matching your selected keyword, performs a sentiment analysis, and prints the info to the screen. Its pretty fast, assuming your keyword query isn't too obscure.

- **tweet_mapper.py** does the exact same thing, but also plots the tweets, color-coded by sentiment (green = positive) on a map of North America. This code can be slow because not that many twitter users include the needed geographical info.

#### How to use this code

The files juts contain a bunch of lines of python code. Either run from command line with, e.g. "python tweet_analyzer.py", or copy and cpaste them into an ipython session. 

Be sure to read the comments at the top of each file, and set the variables for how many tweets you want, keywords to query. You must also obtain and insert your own twitter keys and tokens. See the [Twitter developers site](https://dev.twitter.com/oauth/overview/application-owner-access-tokens).