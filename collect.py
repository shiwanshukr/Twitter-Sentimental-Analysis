#!/usr/bin/env python
# coding: utf-8

# In[12]:


import re 
import tweepy 
import twitter
from tweepy import OAuthHandler 
from matplotlib import pyplot as plt
#import pandas as pd
from TwitterAPI import TwitterAPI
import csv
from collections import Counter
import networkx as nx
import sys
import os
import re
import time
from TwitterAPI import TwitterAPI
import itertools

global max_id

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


def get_tweet_1(twitter,query):

    list_tweet = []
    #query = "trump"
    new_query = query + " -filter:retweets" #This will help to remove Retweets
    tweets = tweepy.Cursor(twitter.search,q=new_query, tweet_mode='extended', lang="en").items(2000)

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
    with open("Collected_Data"+os.path.sep+query+".csv",'w') as wp:
        csv_writer = csv.writer(wp)
        csv_writer.writerow(["Tweet Text", "Sentiment Label"])
        for item in list_tweet:
            #print(item)
            clean_tweet = tweet_cleaner(item.values())
            #print(clean_tweet)
            csv_writer.writerow([clean_tweet]) #item.values()

            #csv_writer.writerow([tweet_dict["id_str"],tweet_dict["text"]])
    wp.close()
    collector_details(len(list_tweet))
    print("❂❂❂❂❂❂❂❂❂ File for ",query,"created Successfully! ❂❂❂❂❂❂❂❂❂")
    
def collector_details(No_of_tweets):
   
    with open("Collected_Data"+os.path.sep +"collected_Data.txt",'w') as fp:
        #fp.write("No of Users Collected : " + str(No_of_users) +"\n")
        fp.write("No of messages Collected : " + str(No_of_tweets)+"\n")

    fp.close()    
    

def get_twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

#################################################################################################
#################################################################################################

class twitter_handler(object):
    def __init__(self): 
        
        try: 
            #==============================Twitter Tokens==========================#
            consumer_key= 'O062S27yXGUh5y1qtoY3SX6Mc'
            consumer_secret= '7GFZ7qjRujuLOiRMWTjeBkTX0iPrC9agRwrMobQUBT15HptyUF'
            access_token= '2723937392-wOjCn19YOotqPGjfbp2MGkzGtGIu9oBELpHNa5H'
            access_token_secret= 'gpaLAjMXmp4RbCx5AYDVqNwaZMEoPvmEznGyACfUvDbhB'
            #======================================================================#
            auth = OAuthHandler(consumer_key, consumer_secret) 
            auth.set_access_token(access_token, access_token_secret) 
            api = tweepy.API(auth) 
            twitter = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
            print(twitter)
        except: 
            print("E.rror!")
        #global twitter
        twitter = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
        

    def robust_request(twitter, resource, params, max_tries=7000):

        """ If a Twitter request fails, sleep for 15 minutes.
        Do this at most max_tries times before quitting.
        Args:
          twitter .... A TwitterAPI object.
          resource ... A resource string to request; e.g., "friends/ids"
          params ..... A parameter dict for the request, e.g., to specify
                       parameters like screen_name or count.
          max_tries .. The maximum number of tries to attempt.
        Returns:
          A TwitterResponse object, or None if failed.
        """
        for i in range(max_tries):
            request = twitter.request(resource, params)
            if request.status_code == 200:   
                return request

    def clean_tweet(tweet):
        a =  (re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())
        return " ".join(a)





    def get_tweets(self): 

        # empty list to store parsed tweets 
        next_max_id=0
        tweets = [] 
        users = ['realDonaldTrump','HillaryClinton','MichelleObama']
        new_max_ids = [0,0,0]
        outfile = open("Cluster_Folder"+os.path.sep+"cluster_testData"+".csv",'a')
        writer = csv.writer(outfile)
        outfile.write('Text\n')
        outfile.close()
        try: 

            # call twitter api to fetch tweets
            while not all(elem == -1 for elem in new_max_ids):
                for user in users:
                    if(new_max_ids[users.index(user)]== -1):
                        continue
                    elif (new_max_ids[users.index(user)] == 0):
                        #print('1')
                        fetched_tweets = twitter_handler.robust_request(twitter, resource='search/tweets', 
                                                         params={'q': user, 'count' : 100}).json()
                    else:
                        resource = 'search/tweets'
                        #print('2')
                        fetched_tweets = twitter_handler.robust_request(twitter, resource,
                                             params={'max_id':new_max_ids[users.index(user)],'q': user, 'count' : 100}).json() 

                    #print("fetched tweets",fetched_tweets)
                    #print("reched 1")
                    if 'next_results' in fetched_tweets['search_metadata']:
                        next_results = fetched_tweets['search_metadata']['next_results']
                        next_max_id = next_results.split('max_id=')[1].split('&')[0]
                        new_max_ids[users.index(user)] = next_max_id
                    else: 
                        new_max_ids[users.index(user)] = -1
                    #print("reached 2")
                    unique_list = []
                    for k in range(len(fetched_tweets['statuses'])):
                        tw = twitter_handler.clean_tweet((fetched_tweets['statuses'][k]['text']))
                        sn = fetched_tweets['statuses'][k]['user']['location']
                        user_ = fetched_tweets['statuses'][k]['user']['screen_name']
                        
                        unique_list.append((tw,sn,user_))
                    
                    outfile = open("Cluster_Folder"+os.path.sep+"cluster_testData"+".csv",'a')
                    writer = csv.writer(outfile)

                    for tup in unique_list:

                        x = tup[0]
                        y = tup[1]
                        z = tup[2]
                        y = y.rstrip('\n')
                        y = y.lstrip('\n')
                        z = z.rstrip('\n')
                        z = z.lstrip('\n')
                        if x.strip().startswith("RT")==False and x!="" and y!="" :        
                            writer.writerow ([x,user,y,z])
                    outfile.close()
                    print("A new csv File successfully ..being created inside the folder Cluster_Folder")
                    print("Loading...file..More data added, wait atleast for a 30 secs")

            return tweets

        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 





            
def main(): 



    #==============================Twitter Tokens==========================#
    consumer_key= 'O062S27yXGUh5y1qtoY3SX6Mc'
    consumer_secret= '7GFZ7qjRujuLOiRMWTjeBkTX0iPrC9agRwrMobQUBT15HptyUF'
    access_token= '2723937392-wOjCn19YOotqPGjfbp2MGkzGtGIu9oBELpHNa5H'
    access_token_secret= 'gpaLAjMXmp4RbCx5AYDVqNwaZMEoPvmEznGyACfUvDbhB'
    #======================================================================# 

print("*********ENTER  1  FOR DOWNLOADING TEST DATA FOR CLASSIFICATION AND \n ENTER  2  FOR DOWNLOADING CLUSTER DATA FOR CLUSTER CLASSIFICATION*****")
print("Once you create your file for either classification or clustering , you can rerun the file to download other set of data")

user_input = input()

if user_input == "1":

    api = get_twitter_api()
    print("Hold on.. Data DOWNLOADING... waiting time less than 2.5 minutes")
    query = ["trump"]
    for i in range(len(query)):
        list_tweet = get_tweet_1(api,query[i])
        create_csv_File(query[i],list_tweet)


###################################################################################################

else:

    #twitter = authenticate(consumer_key,consumer_secret,access_token,access_token_secret) 

    # calling function to get tweets
    api1 = twitter_handler()
    tweets1 = api1.get_tweets()


if __name__ == "__main__": 
# calling main function 
    main() 


# In[ ]:




