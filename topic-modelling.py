import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import random
import nltk
import re
import string
from bs4 import BeautifulSoup

data = pd.read_csv("java_house_sentiments.csv")
data.columns = [
    "Title",
    "Link",
    "Description",
    "Time",
    "Sentiment",
    "Sentiment-Score",
    "Type",
    "Source",
    "Category",
]

# print(data.head())
data.head()

# data.info()
# print(data["Sentiment"].value_counts())

string.punctuation
# print("Punctuation:", string.punctuation)

space_replace = re.compile("[/(){}\[\]\|@,;]")
bad_symbols = re.compile("[^0-9a-z #+_]")
stopwords = ["brt", "rt"]
urls = re.compile(
    "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
    "[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    "rt"
)
usernames = re.compile("@[A-Za-z0-9]+")
# print(usernames)


def text_cleaning(text):
    text = usernames.sub(" ", text)  # removing usernames
    text = BeautifulSoup(text, "lxml").text  # removing any html decoding
    text = text.lower()  # removing capitalization
    text = space_replace.sub(" ", text)  # replacing symbols with a space
    text = bad_symbols.sub("", text)  # deleting symbols from the text
    text = " ".join(
        word for word in text.split() if word not in stopwords
    )  # removing stopwords
    text = urls.sub("", text)  # removing urls
    text = "".join([char for char in text if char not in string.punctuation])
    return text


# data["cleaned_text"] = data["Title"].head().apply(text_cleaning)

# print(data["Title"].head())
# print(data.head())

# CREATING A VOCUBLARY FROM THE DATA USING COUNT VECTORIZER
count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words="english")
term_matrix = count_vect.fit_transform(
    data["Title"].values.astype("U")
)  # including words that occur less than 80% of the time in the document
"""stop words have also been removed since they barely contribute significantly to the vocabulary"""
term_matrix

# we now use LDA to create topics based on the probability of each word in the document
lda = LatentDirichletAllocation(
    n_components=5, random_state=42
)  # we set n = 5 as our initial guess of topics in the data
lda.fit(term_matrix)

# print(lda.components_)
# print(lda.components_.shape)

# print(lda.components_[0])

# print(count_vect.get_feature_names_out())

# top 50 words in the vocubulary
for i in range(51):
    random_word = random.randint(0, len(count_vect.get_feature_names_out()))
    print(count_vect.get_feature_names_out()[random_word])

# displaying the first topic
first_topic = lda.components_[0]
first_topic  # the output is a vector. From the vector we can then obtain the words from the count_vectorizer feature

# obtaining the top words in the first topic
top_topic_words = first_topic.argsort()[-10:]
for i in top_topic_words:
    print(count_vect.get_feature_names_out()[i])

# displaying the top 20 words in each of the topics
for i, topic in enumerate(lda.components_):
    print(f"Top 10 words for topic #{i}:")
    print([count_vect.get_feature_names_out()[i] for i in topic.argsort()[-20:]])
    print("\n")
