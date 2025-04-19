# Twitter Search Application

## 📌 What is this project?

The **Twitter Search Application** is a robust, full-stack system that enables users to search and analyze tweets based on hashtags, usernames, or keywords. Built during a global event (the COVID-19 pandemic), it ingests large-scale Twitter datasets and supports real-time, dynamic queries through a Flask-based web interface. It integrates both **relational (MySQL)** and **non-relational (MongoDB)** databases, supported by an efficient **caching layer** for fast response and scalability.

---

## 💡 Why did we build it?

During high-impact global events like COVID-19, Twitter becomes a critical platform for public discourse. However, searching and analyzing tweets at scale presents challenges due to the volume and velocity of data. We built this project to:

- Simulate real-world data ingestion and search scenarios
- Build a system that balances **query power** (MySQL) and **flexibility** (MongoDB)
- Optimize real-time analytics through **caching, indexing**, and **data modeling**
- Deliver a user-friendly and insightful platform to explore Twitter trends and user behavior

---

## ⚙️ How does it work?

### 🧱 Architecture Overview

- **Frontend**: Flask app interface that lets users:
  - Search by `#hashtag`, `@username`, or free text
  - Filter by date ranges
  - View top 10 tweets (by likes) and top users (by followers)
- **Backend Database**:
  - `MySQL`: Stores structured data such as user profiles and tweet metadata
  - `MongoDB`: Stores unstructured tweet content and hashtags using JSON-like documents
- **Caching**:
  - Implemented with Python dictionaries and a **Least Recently Used (LRU)** policy
  - **Time-to-Live (TTL)** of 1 hour per entry
  - Includes **persistence** to disk and stale data handling on restart
- **Performance Enhancements**:
  - Indexing strategies in MongoDB (text index on tweet content, increasing index on screen names and hashtags)
  - Efficient data storage using `insert_one()` to simulate real-time ingestion

### 🗃️ Dataset

Two datasets (`corona-out-2` and `corona-out-3`) capture Twitter activity during April 2020:

- Over **120,000 tweets** including original tweets and retweets
- Rich metadata including timestamps, hashtags, likes, retweet counts
- Used to model real-time search behavior during the pandemic

---

## 🎯 What did we achieve?

- ✅ **Integrated system** using Flask, MySQL, and MongoDB to handle different data types efficiently
- ✅ **Real-time querying** with <0.01s cache hits and ~0.10s misses
- ✅ Implemented **search filtering** by hashtag, user, and text
- ✅ Built advanced **indexing and cache** systems to reduce latency
- ✅ Designed a responsive, user-friendly GUI to explore data intuitively

---

## 📈 Key Features

- 🔎 Search by hashtag `#`, username `@`, or text
- 📅 Filter tweets by date range
- 🏆 View top 10 tweets and top users
- 🚀 High-performance caching and indexing
- 🧵 Real-time tweet ingestion simulation
- 🧩 Dual-database integration

---

## 📚 Technologies Used

- Python (Flask)
- MySQL
- MongoDB
- Pandas
- JSON
- Twitter data (CSV/Text ingestion)

---

## 📌 Future Enhancements

- Real-time Twitter API integration
- NLP for sentiment and emotion analysis
- Word cloud and topic modeling
- User network graph (influence analysis)



