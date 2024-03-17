from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import pymongo

# VADER === Valence Aware Dictionary and sEntiment Reasoner

# === Sentiment Analysis using VADER example 1 ===

# pd.set_option('display.max_colwidth', 0)
# df = pd.read_csv("test.csv", encoding='cp1252')

# analyzer = SentimentIntensityAnalyzer()

# negative = []
# neutral = []
# positive = []

# for n in range(df.shape[0]):
#     title = df.iloc[n,0]
#     description = df.iloc[n, 2]
#     title_analyzed = analyzer.polarity_scores(title)
#     description_analyzed = analyzer.polarity_scores(description)
#     negative.append(((title_analyzed['neg']) + (description_analyzed['neg']))/ 2)
#     neutral.append(((title_analyzed['neu']) + (description_analyzed['neu'])) / 2)
#     positive.append(((title_analyzed['pos']) + (description_analyzed['pos'])) / 2)
# df["Negative"] = negative
# df["Neutral"] = neutral
# df["Positive"] = positive

# pd.set_option('display.max_columns', None)
# print(df.head())

# print(df["Negative"].mean())
# print(df["Neutral"].mean())
# print(df["Positive"].mean())

# === Sentiment Analysis using VADER example 2 ===

# Create a SentimentIntensityAnalyzer object
analyzer = SentimentIntensityAnalyzer()


# Define a function to get the sentiment score
def sentiment_score(sentence):
    score = analyzer.polarity_scores(sentence)
    return score["compound"]


# Read the data from the CSV file
data = pd.read_csv("nairobi_hospital.csv")
data.columns = ["Title", "Link", "Description", "Time"]

# Apply the sentiment_score function to the Title column
data["Sentiment-Score"] = data["Title"].apply(sentiment_score)
data["Sentiment"] = data["Sentiment-Score"].apply(
    lambda x: "positive" if x > 0 else "negative" if x < 0 else "neutral"
)
data["Type"] = "news"
data["Source"] = "Google News"
data["Category"] = "Nairobi Hospital"

# Write the data to a CSV file
document = open("nairobi_hospital_sentiments.csv", "a")
for i in range(len(data)):
    title = data.iloc[i, 0]
    link = data.iloc[i, 1]
    description = data.iloc[i, 2]
    time = data.iloc[i, 3]
    sentiment_score = data.iloc[i, 4]
    sentiment = data.iloc[i, 5]
    source_type = data.iloc[i, 6]
    source = data.iloc[i, 7]
    category = data.iloc[i, 8]
    document.write(
        f"{title},{link},{description},{time},{sentiment_score},{sentiment},{source_type},{source},{category}\n"
    )

    payload = [
        {
            "type": f"{source_type}",
            "source": f"{source}",
            "category": f"{category}",
            "title": f"{title}",
            "link": f"{link}",
            "description": f"{description}",
            "time": f"{time}",
            "sentiment_score": f"{sentiment_score}",
            "sentiment": f"{sentiment}",
        }
    ]

    # Connect to your MongoDB server
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["sentiment-analysis"]
    collection = database["analyzed-sentiments"]

    # Insert data into MongoDB collection
    collection.insert_many(payload)

document.close()


# Print the data
print(data)
print("Sentiment analysis completed successfully!")
