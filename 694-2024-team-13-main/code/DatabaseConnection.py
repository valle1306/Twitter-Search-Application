#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 02:12:42 2024

@author: manasarthak

"""
# database_connection.py
import mysql.connector
from pymongo import MongoClient
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

def mysql_query(query, params):
    conn = mysql.connector.connect(
        host='localhost', user='root', password='wellplayed666', database='twitter_datasets'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def mongo_query(query, sort_field=None, limit=None, page=None):
    client = MongoClient("mongodb://localhost:27017")
    db = client['dbms_project']
    collection = db['tweets']
    results = collection.find(query)
    if sort_field:
        results = results.sort(sort_field, -1)
    if page and limit:
        results = results.skip((page - 1) * limit).limit(limit)
    elif limit:
        results = results.limit(limit)
    final_results = list(results)
    client.close()
    return final_results

def mongo_aggregate(pipeline):
    client = MongoClient("mongodb://localhost:27017")
    db = client['dbms_project']
    collection = db['tweets']
    try:
        results = collection.aggregate(pipeline)
        final_results = list(results)
        return final_results
    finally:
        client.close()

