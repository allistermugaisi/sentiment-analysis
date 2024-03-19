from flask import request
from app_backend import app
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64
import pymongo
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@app.route("/")
def home():
    return "Welcome to python-flask sentiment analysis model api."


# Display web scraped data and return json
@app.route("/web-scraping")
def webScraping():
    # Connect to your MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["sentiment-analysis"]
    collection = database["web-scraped-data-now"]
    # Retrieve data from MongoDB
    cursor = collection.find({})
    # Convert cursor to list of dictionaries
    data_list = list(cursor)
    # Convert list of dictionaries to JSON
    json_data = json.dumps(data_list, default=str)
    results = json.loads(json_data)

    return results


# Display sentiment analysis data and return json
@app.route("/sentiment-analysis")
def sentimentAnalysis():
    # Connect to your MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["sentiment-analysis"]
    collection = database["analyzed-sentiments-now"]
    # Retrieve data from MongoDB
    cursor = collection.find({})
    # Convert cursor to list of dictionaries
    data_list = list(cursor)
    # Convert list of dictionaries to JSON
    json_data = json.dumps(data_list, default=str)
    results = json.loads(json_data)

    return results


# Display sentiment analysis data and return json
@app.route("/sentiment-analysis/<string:category>")
def sentimentAnalysisCategory(category):
    # Connect to your MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["sentiment-analysis"]
    collection = database["analyzed-sentiments"]
    # Retrieve data from MongoDB
    cursor = collection.find({"category": category})
    # Convert cursor to list of dictionaries
    data_list = list(cursor)
    # Convert list of dictionaries to JSON
    json_data = json.dumps(data_list, default=str)
    results = json.loads(json_data)

    return results


@app.route("/sentiment-analysis/text-prompt/<string:text>")
def sentimentAnalysisTextPrompt(text):
    # Analyze sentiment of the text
    sentiment_label, compound_score = analyze_sentiment(text)

    # Return the sentiment label and compound score
    return json.dumps(
        {"sentiment_label": sentiment_label, "compound_score": compound_score}
    )


def analyze_sentiment(text):
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Analyze sentiment of the text
    sentiment_scores = analyzer.polarity_scores(text)

    # Determine sentiment label based on compound score
    compound_score = sentiment_scores["compound"]
    if compound_score >= 0.05:
        sentiment_label = "Positive"
    elif compound_score <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return sentiment_label, compound_score
