#!/usr/bin/env python
# coding: utf-8

# In[73]:


import twitter
import csv
import tweepy
from TwitterAPI import TwitterAPI
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
import re
import time
from TwitterAPI import TwitterAPI
import itertools

#==============================Twitter Tokens==========================#
consumer_key= 'O062S27yXGUh5y1qtoY3SX6Mc'
consumer_secret= '7GFZ7qjRujuLOiRMWTjeBkTX0iPrC9agRwrMobQUBT15HptyUF'
access_token= '2723937392-wOjCn19YOotqPGjfbp2MGkzGtGIu9oBELpHNa5H'
access_token_secret= 'gpaLAjMXmp4RbCx5AYDVqNwaZMEoPvmEznGyACfUvDbhB'
#======================================================================#

tweets =[]
def get_twitter():
    twitter = TwitterAPI(consumer_key,consumer_secret,access_token,access_token_secret)
    return twitter
twitter = get_twitter()

#request = twitter.request('search/tweets', {'q': 'rahul gandhi','count':200,'lang':'en'})
#tweets = [r for r in request]


def get_tweet(twitter,query):

    list_tweet = []
    #query = "trump"
    new_query = query + " -filter:retweets" #This will help to remove Retweets
    tweets = tweepy.Cursor(twitter.search,q=new_query, tweet_mode='extended', lang="en").items(300)

    for tweet in tweets:
        tweets_dict = {}
        if tweet.full_text not in tweets_dict:
            tweets_dict['text'] = tweet.full_text
            list_tweet.append(tweets_dict)
    #print(list_tweet)
    #for item in list_tweet:
    #    print(item["text"])
    return list_tweet

#********************************CLEANING OF DATA***************************************
def tweet_cleaner(jargons):
    
    in_list = list(jargons)
    jargons = "".join(in_list)
    jargons = str(jargons.lower())
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)+"," ",jargons).split())
    #clean_tweet = re.sub(r'@\w+','',text,flags=re.MULTILINE).split()
    clean_tweet = str(text)
    return str(clean_tweet)
#********************************CLEANING OF DATA***************************************

#**********************Create CSV File **************************************
def create_csv_File(query,list_tweet):
    with open("Extra_Training_Data"+os.path.sep+query+".csv",'w') as wp:
        csv_writer = csv.writer(wp)
        csv_writer.writerow(["Tweet Text", "Sentiment Label"])
        for item in list_tweet:
            #print(item)
            clean_tweet = tweet_cleaner(item.values())
            #print(clean_tweet)
            csv_writer.writerow([clean_tweet]) #item.values()

            #csv_writer.writerow([tweet_dict["id_str"],tweet_dict["text"]])
    wp.close()
    print("File for ",query,"created!")
    
    
    

def get_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


api = get_twitter_api()

#print(get_tweet(api))
#query = ["trump","Hillary Clinton","Michelle Obama"]
query = ["trump"]
for i in range(len(query)):
    list_tweet = get_tweet(api,query[i])
    create_csv_File(query[i],list_tweet)

    



# In[ ]:




