#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 02:12:42 2024

@author: manasarthak
"""

# search_application.py
from DatabaseConnection import mysql_query, mongo_query, mongo_aggregate
from lrucache import cache
import time
from pprint import pprint
from dateutil import parser
import os
import json


# Convert string dates to MongoDB datetime objects
def parse_dates(start, end):
    if start and end:
        try:
            return {'$gte': parser.parse(start), '$lte': parser.parse(end)}
        except Exception as e:
            print(f"Error parsing dates: {e}")
    return {}


def perform_search(query_type, query, page=1, per_page=10, start_time=None, end_time=None):
    cache_key = f"{query_type}:{query}:{page}"
    start_cache_time = time.time()
    cache_result = cache.get(cache_key)
    end_cache_time = time.time()
    if cache_result:
        elapsed_time = end_cache_time - start_cache_time
        print(f"Cache hit for {query}, fetched in {elapsed_time:.2f} seconds")
        return cache_result

    print(f"Cache miss for {query}")
    search_start_time = time.time()

    date_filter = parse_dates(start_time, end_time)
    result = []
    if query_type == 'user':
        user_query = """
            SELECT * FROM Users WHERE screen_name LIKE %s 
            ORDER BY followers_count DESC LIMIT %s, %s
        """
        offset = (page - 1) * per_page
        user_data = mysql_query(user_query, (f"%{query}%", offset, per_page))

        # Extract screen names to use in the MongoDB query
        screen_names = [user['screen_name'] for user in user_data]

        # Create a MongoDB query using the `$in` operator
        tweet_query = {
            'user.screen_name': {'$in': screen_names},
            **({} if not start_time and not end_time else {'created_at': {'$gte': start_time, '$lte': end_time}})
        }
        tweets = mongo_query(tweet_query, 'favorite_count',
                             10 * len(screen_names))  # Assuming you want top 10 tweets per user

        # Map tweets back to users
        for user in user_data:
            user['tweets'] = [tweet for tweet in tweets if tweet['user']['screen_name'] == user['screen_name']]
            result.append(user)

    elif query_type == 'text':
        text_query = {'$text': {'$search': query}, **date_filter}
        result = mongo_query(text_query, 'favorite_count', per_page, page)

    elif query_type == 'hashtag':
        hashtag_query = {'hashtags': query, **date_filter}
        result = mongo_query(hashtag_query, 'favorite_count', per_page, page)

    search_end_time = time.time()
    search_duration = search_end_time - search_start_time
    print(f"Search completed in {search_duration:.2f} seconds")
    cache.put(cache_key, result)
    return result


# Function to get top 10 users based on follower count
def top_10_users():
    user_query = "SELECT * FROM Users ORDER BY followers_count DESC LIMIT 10"
    return mysql_query(user_query, ())


# Function to get top 10 tweets based on favorite count
def top_10_tweets():
    tweet_query = [{'$project': {'tweet_id': 1, 'text': 1, 'favorite_count': 1}},
                   {'$sort': {'favorite_count': -1}},
                   {'$limit': 10}]
    return mongo_aggregate(tweet_query)


# Function for drill-down on tweet metadata from MySQL
def tweet_metadata(tweet_id):
    tweet_query = "SELECT * FROM Tweets WHERE tweet_id = %s"
    return mysql_query(tweet_query, (tweet_id,))


# Function for drill-down on user activity based on screen name
def user_activity(screen_name, limit=10):
    user_query = "SELECT * FROM Users WHERE screen_name = %s"
    user_data = mysql_query(user_query, (screen_name,))

    tweet_query = {
        'user.screen_name': screen_name
    }
    user_data['tweets'] = mongo_query(tweet_query, 'favorite_count', limit)

    return user_data


# Example usages of the functions
if __name__ == "__main__":

    if not os.path.exists('cache.json'):
        with open('cache.json', 'w') as f:
            json.dump({}, f)  # Create an empty JSON object

    # last _persisted_cache
    print("peristed_cache")
    cache.print_cache()
    # Example search by text
    search_results_text = perform_search('text', 'coffee')
    print("Text Search Results:")
    pprint(search_results_text)

    # Example search by hashtag for "COVID19InTurkeysPrisons"
    search_results_hashtag = perform_search(
        query_type='hashtag',
        query='COVID19InTurkeysPrisons')
    print("\nHashtag Search Results:")
    pprint(search_results_hashtag)

    # Example search by user
    search_results_user = perform_search('user', 'Alice')
    print("\nUser Search Results:")
    pprint(search_results_user)

    print("updated_cache")
    cache.print_cache()

    # Fetching and displaying top 10 users
    top_users = top_10_users()
    print("\nTop 10 Users:")
    pprint(top_users)

    # Fetching and displaying top 10 tweets
    top_tweets = top_10_tweets()
    print("\nTop 10 Tweets:")
    pprint(top_tweets)

    cache.persist()
