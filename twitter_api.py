import tweepy
import hconfig
import json
import pandas as pd

def twitter_client():
    client = tweepy.Client(bearer_token=hconfig.bearer_token,
                           consumer_key=hconfig.consumer_key, consumer_secret=hconfig.consumer_secret, access_token=hconfig.access_token, access_token_secret=hconfig.access_secret)
    return client

def search_tweets(keywords):
    client = twitter_client()
    tweets = client.search_recent_tweets(query=keywords, max_results=10)

    data = tweets.data
    results = pd.DataFrame(columns = ['id','text'])

    if data:
        for tweet in data:
            obj = {}
            obj['id'] = tweet.id
            obj['text'] = tweet.text
            results = results.append(obj, ignore_index = True)
    else:
        return ''

    return results

tweets = search_tweets("bitcoin ransomware")
print(tweets)