from pymongo import MongoClient
from bson import json_util
import json
from TimedSearch import perform_search


class ExternalDataProvider:
    def __init__(self):
        self.MONGODB_URL = "mongodb://localhost:27017"
        self.client = MongoClient(self.MONGODB_URL)
        self.tweets_collection = self.client.dbms_project.tweets

    def get_tweets_by_user(self, query, page=1, per_page=10):
        """
        Search user by username and screen name, return json data
        :param page:
        :param per_page:
        :param query: username or screen name
        :return: list of dict, contain 'name', 'screenName', 'description', 'link'
        """
        raw_results = perform_search('user', query, page, per_page)

        people = []
        all_tweets = []
        for user in raw_results:
            user_dict = {
                'name': user.get('name'),
                'screenName': user.get('screen_name'),
                'followers': user.get('followers_count', '')
            }
            people.append(user_dict)

            tweets = user.get('tweets')
            for tweet in tweets:
                tweet['tweet_id'] = str(tweet.get('tweet_id'))
            all_tweets.extend(tweets)
        result = {
            'people': people,
            'tweets': all_tweets
        }
        return json.loads(json_util.dumps(result))

    def get_tweets_by_text(self, query, page=1, per_page=10):
        """
        :param page: page number
        :param per_page: items per page
        :param query: keywords in text
        :return: list of dict, contains 'name', 'screenName', 'content', 'timestamp'
        """

        people = []
        raw_results = perform_search('text', query, page, per_page)
        for result in raw_results:
            result['tweet_id'] = str(result.get('tweet_id'))
        result = {
            'people': people,
            'tweets': raw_results
        }

        return json.loads(json_util.dumps(result))

    def get_tweets_by_hashtag(self, query, page=1, per_page=10):
        """
        Search tweets by hashtag, return json data
        :param query: hashtag without #
        :param page: page number
        :param per_page: items per page
        :return: list of dict
        """

        people = []
        raw_results = perform_search('hashtag', query, page, per_page)
        for result in raw_results:
            result['tweet_id'] = str(result.get('tweet_id'))
        result = {
            'people': people,
            'tweets': raw_results
        }
        return json.loads(json_util.dumps(result))


data_provider = ExternalDataProvider()
