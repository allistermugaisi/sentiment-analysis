import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Embedding,
    Conv1D,
    GlobalMaxPooling1D,
    Dense,
    Dropout,
)
import pickle5 as pickle


# Load the dataset
df = pd.read_csv("results.csv")
# print(df.head())

# # Split the dataset into training and testing
# X = df["description"]
# y = df["sentiment"]
# # X_train, X_test, y_train, y_test = train_test_split(
# #     X, y, test_size=0.2, random_state=42
# # )

# # Tokenize the dataset
# tokenizer = Tokenizer(num_words=10000)
# tokenizer.fit_on_texts(X_train)
# X_train = tokenizer.texts_to_sequences(X_train)
# X_test = tokenizer.texts_to_sequences(X_test)

# # Pad the dataset
# X_train = pad_sequences(X_train, padding="post", maxlen=256)
# X_test = pad_sequences(X_test, padding="post", maxlen=256)

# # Load the word embeddings
# embeddings_index = {}
# with open("glove.6B.100d.txt", encoding="utf8") as f:
#     for line in f:
#         values = line.split()
#         word = values[0]
#         coefs = np.asarray(values[1:], dtype="float32")
#         embeddings_index[word] = coefs

# # Create the embedding matrix
# embedding_matrix = np.zeros((10000, 100))
# for word, i in tokenizer.word_index.items():
#     if i < 10000:
#         embedding_vector = embeddings_index.get(word)
#         if embedding_vector is not None:
#             embedding_matrix[i] = embedding_vector

# # Create the model
# model = Sequential()
# model.add(
#     Embedding(10000, 100, input_length=256, weights=[embedding_matrix], trainable=False)
# )
# model.add(Conv1D(128, 5, activation="relu"))
# model.add(GlobalMaxPooling1D())
# model.add(Dense(10, activation="relu"))
# model.add(Dropout(0.5))
# model.add(Dense(1, activation="sigmoid"))

# # Compile the model
# model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# # Train the model
# history = model.fit(X_train, y_train, epochs=5, validation_data=(X_test, y_test))

# # Save the model
# model.save("sentiment_model.h5")

# # Save the tokenizer
# with open("tokenizer.pkl", "wb") as f:
#     pickle.dump(tokenizer, f)

# # Save the history
# with open("history.pkl", "wb") as f:
#     pickle.dump(history.history, f)
