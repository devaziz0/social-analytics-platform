
from flask import Flask
from flask import request
from langdetect import detect
import pandas as pd


# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, Embedding, Flatten, Conv1D, MaxPooling1D, LSTM
from keras import utils
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.models import load_model

# Word2vec
import gensim
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
# Utility
import re
import numpy as np
import os
from collections import Counter
import logging
import time
import pickle
import itertools
import tensorflow as tf
graph = tf.get_default_graph()
# Set log
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# DATASET
DATASET_COLUMNS = ["target", "ids", "date", "flag", "user", "text"]
DATASET_ENCODING = "ISO-8859-1"
TRAIN_SIZE = 0.8

# TEXT CLENAING
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

# WORD2VEC
W2V_SIZE = 300
W2V_WINDOW = 7
W2V_EPOCH = 32
W2V_MIN_COUNT = 10

# KERAS
SEQUENCE_LENGTH = 300
EPOCHS = 8
BATCH_SIZE = 1024

# SENTIMENT
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

# EXPORT
KERAS_MODEL = "model.h5"
WORD2VEC_MODEL = "model.w2v"
TOKENIZER_MODEL = "tokenizer.pkl"
ENCODER_MODEL = "encoder.pkl"

decode_map = {0: "NEGATIVE", 2: "NEUTRAL", 4: "POSITIVE"}


def decode_sentiment(label):
    return decode_map[int(label)]


w2v_model = model = Word2Vec.load("/opt/model.w2v")


words = w2v_model.wv.vocab.keys()
vocab_size = len(words)

w2v_model.most_similar("love")


with open('/opt/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
handle.close()


with open('/opt/encoder.pkl', 'rb') as handle:
    encoder = pickle.load(handle)

handle.close()

model = load_model('/opt/model.h5')


def decode_sentiment(score, include_neutral=True):
    if include_neutral:
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE

        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE


def predict(text, include_neutral=True):
    start_at = time.time()
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences(
        [text]), maxlen=SEQUENCE_LENGTH)
    # Predict
    with graph.as_default():
        score = model.predict([x_test])[0]
    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    return {"label": label, "score": float(score),
            "elapsed_time": time.time()-start_at}


app = Flask(__name__)


@app.route('/')
def hello():
    count = 4
    return predict("i don't know what i'm doing")


@app.route('/predict/', methods=['POST', 'GET'])
def predict_view():
    error = None
    if request.method == 'POST':
        msg = request.form['message']
        print(msg)
        return predict(msg)


@app.route('/predict-multiple/', methods=['POST', 'GET'])
def predict_batch_view():
    error = None

    if request.method == 'POST':

        msgs_list = request.get_json()

        response = {"NEGATIVE": 0, "POSITIVE": 0, "NEUTRAL": 0, }

        for message in msgs_list:
            try:
                lang = detect(message)
            except:
                lang = ''

            # Only do prediction on english messages
            if lang == 'en':
                result = predict(message)

                if result['label'] == "NEGATIVE":
                    response['NEGATIVE'] += 1
                elif result['label'] == "NEUTRAL":
                    response['NEUTRAL'] += 1
                elif result['label'] == "POSITIVE":
                    response['POSITIVE'] += 1

        return response
