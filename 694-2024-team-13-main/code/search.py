# +
import mysql.connector
from mysql.connector import Error

def create_database_connection():
    try:
        config = {
          'user': 'root',
          'password': 'wellplayed666',
          'host': 'localhost',
          'database': 'twitter_datasets',
          'raise_on_warnings': True
        }
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


# +
import mysql.connector

class MySQLSearcher:
    def __init__(self, config):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def search_by_user(self, user):
        query = '''
        SELECT * FROM Users
        WHERE name LIKE CONCAT('%', %s , '%')
        OR screen_name LIKE CONCAT('%', %s , '%')
        ORDER BY name;
        '''
        self.cursor.execute(query, (user, user))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    config = {
      'user': 'root',
      'password': 'wellplayed666',
      'host': 'localhost',
      'database': 'twitter_datasets',
      'raise_on_warnings': True
    }
    db = MySQLSearcher(config)

    results = db.search_by_user('joe')

    for row in results:
        print(row)

    db.close()


# +
from pymongo import MongoClient

class TweetSearcher:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def search_by_text(self, text):
        """ search by content """
        results = self.collection.find({"text": {"$regex": text, "$options": "i"}})
        return list(results)

    def search_by_hashtag(self, hashtag):
        """ search tweet by hashtag """
        results = self.collection.find({"hashtags": {"$elemMatch": {"text": hashtag}}})
        return list(results)

    def close(self):
        """ close database connection """
        self.client.close()

if __name__ == "__main__":
    db_url = ""
    db_name = ""
    collection_name = ""

    searcher = TweetSearcher(db_url, db_name, collection_name)
    text_search_results = searcher.search_by_text("text")
    hashtag_search_results = searcher.search_by_hashtag("hashtag")

    print("Text search results:")
    for tweet in text_search_results:
        print(tweet)

    print("\nHashtag search results:")
    for tweet in hashtag_search_results:
        print(tweet)

    searcher.close()

