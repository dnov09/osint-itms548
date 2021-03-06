# -*- coding: utf-8 -*-
"""
@authors: David Ngige, Hareem Akram & Rida Tariq

"""

import praw
import csv
import datetime
from hconfig import c_id, secret, usr, pwd, agent
import pandas as pd

# Reddit Functions
def credentials():
    reddit = praw.Reddit(
        username=usr,
        password=pwd,
        client_id=c_id,
        client_secret=secret,
        user_agent=agent,
    )
    return reddit

# function to pull data
def get_data(keywords,maxresults=100):
    reddit = credentials()
    subreddit = reddit.subreddit("all")
    data_pool = subreddit.search(keywords, limit=maxresults, time_filter="year")

    rv = {}
    post_id = []
    subred = []
    post_title = []
    num_com = []
    post_auth = []
    post_date = []
    post_date_utc = []

    for keywords in data_pool:
        # add the posts to our dict as they are being called
        rv[keywords.title] = {
            "post_id": keywords.id,
            "subreddit": keywords.subreddit,
            "title": keywords.title,
            "num_comments": keywords.num_comments,
            "author": keywords.author,
            "date_posted": to_datetime(keywords.created_utc)
        }

        post_id.append(keywords.id)
        subred.append(keywords.subreddit)
        post_title.append(keywords.title)
        num_com.append(keywords.num_comments)
        post_auth.append(keywords.author)
        post_date.append(to_datetime(keywords.created_utc))
        post_date_utc.append(keywords.created_utc)

    # sending to csv
    df = pd.DataFrame({'ID': post_id,
                       'Author': post_auth,
                       'Subreddit': subred,
                       'Title': post_title,
                       'Number of comments': num_com,
                       'Time Posted': post_date,
                       'UTC': post_date_utc
                       })

    df.to_csv('reddit_dataset.csv', index=False)
    return rv

def to_datetime(utc_time):
    
    # converting utc to regular datetime
    return datetime.datetime.fromtimestamp(utc_time)
