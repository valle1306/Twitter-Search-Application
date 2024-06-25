from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client['twitter']
tweets_collection = db['tweets']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    cursor = tweets_collection.find({"$text": {"$search": query}}).limit(20)
    results = list(cursor)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
